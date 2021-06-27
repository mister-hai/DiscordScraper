# -*- coding: utf-8 -*-
################################################################################
## Message Scraper for discord archival                                       ##
################################################################################
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
"""
Discord bot message archival
    --saveformat sets the defaults save format

"""
TESTING = True
import sys,os
import requests
from time import sleep
from io import BytesIO
from pathlib import Path

from urllib.parse import urlparse
from requests import requote_uri


from src.util import redprint,blueprint,greenprint,errormessage,debugmessage
from src.util import warn,yellowboldprint,defaultheaders,makered

class ParentClass(object):
    def __new__(cls, *args, **kwargs):
        return super(__class__, cls).__new__(cls, *args, **kwargs)
    def __init__(self):
        self.data = {}
    def __call__(self):
        return self.data

class ChildClass(ParentClass):
    def __new__(cls, *args, **kwargs):
        print(super(__class__, cls).__new__(cls, *args, **kwargs))
    def __init__(self):
        self.data = {}
    def __call__(self):
        print("class name: " + self.__class__)

class DiscordAuth(requests.auth.AuthBase):
    def __new__(cls, *args, **kwargs):
        #default fake value
        cls.discord_bot_token   = "NzE0NjA3NTAyOTg1MDAzMDgw.XxV-HQ.mn5f97TDYXtuFVgTwUccfsW4Guk"
        return super(DiscordAuth, cls).__new__(cls, *args, **kwargs)

    def __init__(self, discord_bot_token):
        if discord_bot_token:
            self.token = discord_bot_token

    def __call__(self):
        return self.username, self.token

class APIRequest():
    '''uses Requests to return specific routes from a base API url'''
    def __init__(self, apibaseurl:str, thing:str):
        self.request_url = requote_uri("".format(apibaseurl,self.thing))
        blueprint("[+] Requesting: " + makered(self.request_url) + "\n")
        self.request_return = requests.get(self.request_url)
    
    def request(self, url, auth=('user', 'pass')):
        '''makes the actual request'''
        return requests.get(url=url, auth=auth)

    def checkurlagainstdomain(self,urltoscan,listofdomains):
        parsedurl = urlparse(urltoscan)
        qwer = parsedurl.netloc.split('/')[2].split(':')[0]
        if qwer in listofdomains:
            return True
        else:
            return False
    def filtermessage(self,message):
        pass

    def filterattachment(self,attachment,urlfilter = domainlist):
        if (attachment.url != None):
            if (attachment.filename.endswith(".jpg" or ".png" or ".gif")):
                if (self.checkurlagainstdomain(attachment.url, urlfilter)):
                    return True



class HTTPDownloadRequest():
    '''refactoring to be generic, was based on discord, DEFAULTS TO DISCORD AUTHSTRING'''
    def __init__(self,headers:dict, httpauthstring:str,url:str,discord_bot_token = ""):
        self.responsedatacontainer = []
        self.requesturl = url
        self.domainfilterlist = ['discordapp.com', 'discord.com', "discordapp.net"]
        if len(self.headers) > 0:
            self.headers = defaultheaders
        else:
            self.setHeaders(headers)
        # just a different way of setting a default
        # good for long strings as defaults
    # Authorization headers set with headers= will be overridden if credentials 
    #    are specified in .netrc, which in turn will be overridden by the auth= parameter. 
    #    Requests will search for the netrc file at ~/.netrc, ~/_netrc, or at the path 
    # Authorization headers will be removed if you get redirected off-host.
    # Proxy-Authorization headers will be overridden by proxy credentials provided in the URL.
    # Content-Length headers will be overridden when we can determine the length of the content.

    def makerequest(self):
        try:
            # perform the http request
            self.sendRequest(self.requesturl)
            #check to see if there is data
            if self.response == None:
                raise Exception

        except Exception:
            errormessage("[-] Error in HTTPDownloadRequest()")

    def setrequesturl(self,newurl):
        '''sets the url to request from
    now you only need to create one object and call this for each new download'''
        try:
            self.requesturl = newurl
            return True
        except:
            errormessage("[-] Failed to set new URL on HTTPDownloadRequest.url")
            return False
    
    def setHeaders(self, headers):
        self.headers = headers


    def sendRequest(self, url):
        '''first this is called'''
        self.response = requests.get(url, headers=self.headers)
        if TESTING == True:
            for header in self.response.headers:
                if header[0] == 'Retry-After':
                    debugmessage(header)
        #filter out errors with our own stuff first
        if self.was_there_was_an_error(self.response.status_code) == False:
            # Return the response if the connection was successful.
            if 199 < self.response.status_code < 300:
                return self.response
            #run this function again if we hit a redirect page.
            elif 299 < self.response.status_code < 400:
                # Grab the URL that we're redirecting to.
                redirecturl = self.response.header('Location')
                newdomain = redirecturl.split('/')[2].split(':')[0]
                # If the domain is a part of Discord then re-run this function.
                if newdomain in self.domainfilterlist:
                    self.sendRequest(redirecturl)
                # Throw a warning message to acknowledge an untrusted redirect.
                warn('[+] Ignored unsafe redirect to {}.'.format(redirecturl))
            # Otherwise throw a warning message to acknowledge a failed connection.
            else: 
                warn('HTTP {} from {}. Image Download Failed'.format(self.response.status_code, redirecturl))

            # if we need to retry
            # Handle HTTP 429 Too Many Requests
            if self.response.status_code == 429:
                retry_after_time = self.response.headers['retry_after']
                if retry_after_time > 0:   
                    sleep(1 + retry_after_time)
                    self.retryrequest(url)        
            # Return nothing to signify a failed request.
            return None

    def retryrequest(self,url):
        '''and this is sent if we need to retry'''
        self.sendRequest(url)

    def was_there_was_an_error(self, responsecode):
        ''' Basic prechecking before more advanced filtering of output
Returns False if no error
        '''
        # server side error]
        set1 = [404,504,503,500]
        set2 = [400,405,501]
        set3 = [500]
        if responsecode in set1 :
            blueprint("[-] Server side error - No Image Available in REST response")
            yellowboldprint("Error Code {}".format(responsecode))
            return True # "[-] Server side error - No Image Available in REST response"
        if responsecode in set2:
            redprint("[-] User error in Image Request")
            yellowboldprint("Error Code {}".format(responsecode))
            return True # "[-] User error in Image Request"
        if responsecode in set3:
            #unknown error
            blueprint("[-] Unknown Server Error - No Image Available in REST response")
            yellowboldprint("Error Code {}".format(responsecode))
            return True # "[-] Unknown Server Error - No Image Available in REST response"
        # no error!
        if responsecode == 200:
            return False
