
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
pretty sure its making a lot of copies of images in memory, 
I wasnt paying much attention to memory. cleaning up the self.imagearrays
should solve that
"""
from app import timeofrun

import os,re
import pandas
import base64
import discord
import shutil

from src.util import redprint,blueprint,greenprint,warning_message,errormessage
from src.util import scanfilesbyextension
from src.database import DiscordMsgDB,DiscordMessage,addmsgtodb
from src.MessageHandler import MessageHandler
from src.HTTPRequest import HTTPDownloadRequest
from src.ConvertToBase64 import ImageToBase64


class DatabasePacker():
    """General Purpose Pandas linkage between DB and script
    Dataframe to Database Tool,
        Import into a .py file alongside the database.py internals
    
    Dataframe columns translate to flask-sqlalchemy/sqlite3 tables
    """
    def __init__(self,dataframe:pandas.Dataframe):
        self.filterfield = ""
        self.filterstring = ""
        self.dataframe = dataframe
        
    def packdb(self):
        '''packs dataframe to database, use this after populating the frame'''
        try:
            #push to DB
            addmsgtodb(self.messagedataframe)
        except Exception:
            errormessage("[-] DatabasePacker() FAILED")
    
    def packframe(self):
        '''puts the contents of a message into a dataframe for database insertion'''
        try:
            # defaults to discarding empties... there are no empties
            if self.dataframe[self.filterfield] == self.filterstring:
                warning_message("[-] PANDAS - input : {} : discarded from rows".format(self.dataframe[self.filterstring]))
            else :
                self.messagedataframe = DiscordMessage(
                                        channel = self.dataframe['channel'],
                                        time = self.dataframe['time'],
                                        sender = self.dataframe['sender'],
                                        content = self.dataframe['content'],
                                        # either a file path or base64  
                                        file = self.dataframe['file'])
        except Exception:
            errormessage("[-] DatabasePacker() FAILED")                                                               

###############################################################################
#                CHANNEL SCRAPING CLASS
###############################################################################

class DiscordScrape():
    '''Operates inside of a loop, on a single discord.Message
    
    Provide a Handler(filter) and database connection via the database packer
    '''
    def __init__(self,
                 token,
                 username,
                 #dbtype,
                 dbsaveformat:str,
                 msghandler:MessageHandler,
                 #dataframe:pandas.DataFrame,
                 dbpacker : DatabasePacker,
                 current_channel:str,
                 imagesaveformat:str,
                 noimages:bool):
        self.authtoken = token
        self.username = username
        self.noimages = noimages
        self.imgsavefmt = imagesaveformat
        self.handler = msghandler
        self.dbpacker = dbpacker
        self.channel = current_channel
        self.dbsaveformat = dbsaveformat
        #if the message had an image or imageurl
        self.thereisanimage = bool
        self.dictofimages = {}
        self.rawimagedatadict = {}
        self.base64imagedict = {}
        self.timeofrun = timeofrun
        self.imagefolder         = "images/"
        #"./images/channel/imagexxxx-DATE-TIME-sent.png.jpg.b64"
        self.baseimagefolder     = self.imagefolder
        #self.dbtype = dbtype
        #self.dataframe = dataframe

    def processmessageinloop(self,message:discord.Message):
        if self.noimages == False:
            #set the image save location in case of images in the message
            self.imagefolderNOW = self.baseimagefolder +"/"+ self.channel +"/"+ self.timeofrun +"/"
            self.msgtimesent = message.created_at
            self.extractimages(message)
            #put the file to disk if any
            if self.thereisanimage:
                self.processmessageforimages(message)
        # skip the entire previous block 
        # if user requested no images to be saved
        elif self.noimages == True:
            pass
        ############ pack dataframe ########################
        self.dbpacker.dataframe['channel'] = message.channel
        self.dbpacker.dataframe['time']    = message.created_at
        self.dbpacker.dataframe['sender']  = message.author
        self.dbpacker.dataframe['content'] = message.content
        #path to file if file was present
        self.dbpacker.dataframe['file'] = self.DBimageentry
        self.dbpacker.packframe(message=message)
        # shove the info into the db
        self.dbpacker.packdb()
        return True

    def processmessageforimages(self, message:discord.Message):
        self.DBimageentry = []
        if self.dbsaveformat == 'base64': #saving image as text only if argument given
            # turn all images to b64
            for imagename,rawimagedata in self.rawimagedatadict:
                imagedata = ImageToBase64(imagebytes = rawimagedata, imagesaveformat = self.imgsavefmt)
                self.dictofimages[imagename] = imagedata
            for filename in self.dictofimages.keys():
                # set path
                self.DBimageentry = self.imagefolderNOW + filename
                # save file
                self.saveimage(self.dictofimages[filename],self.DBimageentry,filename= filename)
        elif self.dbsaveformat == 'file':
            for name,image in self.dictofimages:
                #set the image field in the db entry to the PATH of the image
                pathstring = self.imagefolderNOW + name
                self.DBimageentry.append(pathstring)
                self.saveimage( data          = image,
                                savedirectory = self.imagefolderNOW,
                                filename      = pathstring) #PATH TO IMAGE

    def saveimage(self,data,savedirectory,filename):
        '''Saves a meggage according to global configuration
        messagedirectoryNOW = messagedirectoryNOW
        '''        
        imagefilename = filename + self.msgtimesent
        try:
            #if the dir not exist
            if os.path.isdir(savedirectory) == False:
                os.makedirs(savedirectory, exist_ok=True)
            #open empty file
            with open(imagefilename,'wb') as out_file:
                #make not empty
                shutil.copyfileobj(data, out_file)
        except Exception:
            errormessage("[-] ERROR Saving Image Data to disk!")

    def grabimage(self,imageurl)->dict:
        '''runs in a loop to download all extracted links in a single message'''
        try:
            newrequest = HTTPDownloadRequest(headers  = "", url = imageurl)
            response = newrequest.makerequest()
            imageresponse = {}
            if "Content-Disposition" in response.headers.keys():
                filename = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
            else:
                filename = imageurl.split("/")[-1]
            imageresponse[filename]= response.content
            return imageresponse
        except Exception:
            errormessage("[-] Failed To Grab Image: {}".format(imageurl))

    def extractimages(self,message:discord.Message):
        '''runs in a loop to extract all image links from a message'''
        attachments = message.attachments
        msgcontent = message.content
        #if there are NO attachments
        if len(attachments) == 0:
            #Scan for urls and tokens identifying an image link
            imagelinks = self.handler.scanforurlinmessage(msgcontent)
            # there is an image or set of images
            if len(imagelinks) > 0 or imagelinks != False:
                self.thereisanimage == True
                for imageurl in imagelinks:
                    #grab image
                    self.rawimagedatadict = self.grabimage(imageurl = imageurl)
                    #self.rawimagedatadict[]
        #process attachments to grab images
        elif len(attachments) > 0:
            self.thereisanimage == True
            for attachment in attachments:
                #domainlist = ['discordapp.com', 'discord.com', "discordapp.net", "imgur.com","rule34.xxx","i.redd.it"]
                if self.handler.filterattachment(domainlist ,attachment):
                    #get raw image data and assign to self for next step
                    self.rawimagedatadict[attachment.filename] = self.grabimage(imageurl = attachment.url)
                else:
                    redprint("[-] Link not in filter! Aborting Operation!")
                    raise Exception
