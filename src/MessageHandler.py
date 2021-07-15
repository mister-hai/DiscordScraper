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

from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
import discord
import re
from discord.ext import commands, tasks


class MessageHandler():
    ''' '''
    def __init__(self, domainlist):
        #self.domainfilterlist = domainlist
        self.domainregex    = [r"(https://cdn\.discordapp\.com)",r"(https://rule34\.xxx)",
                                 r"(https://i\.redd\.it/)",r"(https://imgur.com/)",
                                 r"media.discordapp.net"
                            ]
        self.extensionregex = [r"(\.jpg)",r"(\.png)",r"(\.gif)",r"(\.mp4)",
                               r"(\.avi)", r"(\.jpeg)",r"(\.webm)"
                            ]
        self.goodreggie = r'''(https?:)?\/\/?[^\'"<>]+?\.(jpg|jpeg|gif|png|mp4|webm)'''
        self.regexforimage = re.compile(self.goodreggie)

    def deletemessageifmatch(self,message:discord.Message):
        pass

    def scanforurlinmessage(self,msgcontent:str)->list:
        # if it has multiple image links , return 
        'filters out images from undesired sources, needs a regex that matches to end of extension'
        output = []
        # delimiters are spaces between words, and newlines
        splitbylines = msgcontent.split("\n")
        for lineoftext in splitbylines:
            # check for domains and extensions
            #for regex in self.list_o_reggies:
                if re.match(pattern = self.goodreggie, string = lineoftext):
                    output.append(lineoftext)
        if len(output) > 0:
            return output
        else:
            return False

    def checkurlagainstdomain(self,urltoscan,listofdomains):
        '''logic for allowing the control flow to continue'''
        parsedurl = urlparse(urltoscan)
        domainrequested = parsedurl.netloc.split('/')[2].split(':')[0]
        if domainrequested in listofdomains:
            return True
        else:
            return False

    def filterattachment(self,
                         attachment:discord.Attachment,
                         urlfilter:list,
                         extensionfilter:list):
        '''logic for allowing the control flow to continue'''
        if (attachment.url != None):
            if (attachment.filename.endswith(extensionfilter)):
                if (self.checkurlagainstdomain(attachment.url, urlfilter)):
                    return True