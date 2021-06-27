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
################################################################################
# Imports
################################################################################
print("[+] Starting Discord Scraping Utility")
TESTING = True

import base64
import sys,os
import pandas
import requests
from pathlib import Path
import datetime
from datetime import date
from urllib.parse import urlparse
import discord
from discord.ext import commands, tasks
from src.DatabasePacker import DatabasePacker
from src.HTTPRequest import HTTPDownloadRequest
from src.SaveDiscordImage import SaveDiscordImage
from src.database import DiscordMsgDB,DiscordMessage,addmsgtodb
from src.util import redprint,blueprint,greenprint,errormessage,debugmessage
from src.util import warn,yellowboldprint,warning_message
################################################################################
# Variables
################################################################################
discord_bot_token   = "NzE0NjA3NTAyOTg1MDAzMDgw.XxV-HQ.mn5f97TDYXtuFVgTwUccfsW4Guk"
COMMAND_PREFIX      = "."
bot_help_message = "I AM"
BOT_PERMISSIONS     = 3072
devs                = [712737412018733076]
#cog_directory_files = os.listdir("./things_it_does/cogs")
load_cogs           = False
bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
domainlist = ['discordapp.com', 'discord.com', "discordapp.net"]
attachmentsurl = "/attachments/"
client = discord.Client()
guild = discord.Guild
SAVETOCSV = arguments.saveformat
today = date.today()
###############################################################################
#                        Command Line Arguments
###############################################################################
import argparse
parser = argparse.ArgumentParser(description='Discord Message Archival')
parser.add_argument('--imagestoretype',
                                 dest    = 'saveformat',
                                 action  = "store" ,
                                 default = "file", 
                                 help    = "set if images are saved in the DB as text or externally as files, OPTIONS: 'file' OR 'base64. " )
parser.add_argument('--messagelimit',
                                 dest    = 'limit',
                                 action  = "store" ,
                                 default = "10000", 
                                 help    = "Number of messages to download" )
parser.add_argument('--databasename',
                                 dest    = 'dbname',
                                 action  = "store" ,
                                 default = "discordmessagehistory", 
                                 help    = "Name of the file to save the database as" )
parser.add_argument('--databasetype',
                                 dest    = 'dbtype',
                                 action  = "store" ,
                                 default = "sqlite3", 
                                 help    = "text storage format, can be 'sqlite3' OR 'csv', This applies to base64 image data as well" )
parser.add_argument('--imagesaveformat',
                                 dest    = 'imagesaveformat',
                                 action  = "store" ,
                                 default = ".png", 
                                 help    = "File extension for images" )
arguments = parser.parse_args()


###############################################################################
#                DISCORD COMMANDS
###############################################################################
# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@bot.event
async def on_ready():
    print("Discrod Scraper ALPHA")
    await bot.change_presence(activity=discord.Game(name="Chembot - type .help"))
    #await lookup_bot.connect()

imagesaveformat = ".png"
imagedirectory = os.getcwd() + "/images/"
directory_listing = scanfilesbyextension(imagedirectory,arguments.imagesaveformat)
#function to call the scraper class when ordered
@bot.event
async def scrapemessages(message,channel,limit):
    #get the input
    dbpacker = DatabasePacker()
    #itterate over messages in channel until limit is reached
    for msg in message.channel.history(limit):
        #ain't us
        if msg.author != client.user:
            #wasting memory
            #messageContent = message.content
            messageattachments = message.attachments
            ## creater pandas DF
            data = pandas.DataFrame(columns=['channel', 'sender', 'time', 'content','file'])
            #if self.filtermessage(messageattachments):
            #if attachment exists in message
            if len(messageattachments) > 0:
                #process attachments to grab images
                for attachment in messageattachments:
                    #its a link to something and that link is an image in discords CDN
                    # TODO: add second filter calling a class that checks for discord CDN
                    if (attachment.url != None) and (attachment.filename.endswith(".jpg" or ".png" or ".gif")):
                        # standard headers
                        imagedata = HTTPDownloadRequest("",discord_bot_token,attachment.url)
                        imagesaver = SaveDiscordImage(imagebytes      = imagedata,
                                                      base64orfile    = arguments.saveformat,
                                                      filename        = attachment.name,
                                                      imagesaveformat = arguments.imagesaveformat
                                                    )
                        #base64 specific stuff
                        #if arguments.saveformat == "base64":
                        
                        # if they want to save an image as a file and link to it in the database
                        if arguments.saveformat == "file":
                            # add the time and sender/messageID to name
                            # just in case of data loss
                            file_location = arguments.dbname + "_" + str(datetime.now()) + "_" + msg.author
                        # we now have either base64 image data, or binary image data
                        imageblob = imagesaver.imagedata()
                    else:
                        raise Exception
            #pack info into dataframe
            data = data.append({'channel'      : msg.channel,
                                'sender'       : msg.author.name,
                                'time'         : msg.created_at,
                                'content'      : msg.content,
                                'file'         : imagedata},
                                ignore_index = True)
            #perform data output

            #if they want a CSV file
            if SAVETOCSV == True:
                #file_location = arguments.dbname + str(today) # Set the string to where you want the file to be saved to
                data.to_csv(file_location)
            #i they want to push it to a local sqlite3 database
            elif SAVETOCSV == False:
                messagesent = DiscordMessage(channel = data['channel'],
                                            time     = data['time'],
                                            sender   = data['sender'],
                                            content  = data['content'],
                                            # either a file path or base64 
                                            file     = data['file'])
                #push to DB
                addmsgtodb(messagesent)
                dbpacker.channelscrapetodb(data)
        #stop at message limit
        if len(data) == limit:
            break

    def checkurlagainstdomain(self,urltoscan,listofdomains):
        parsedurl = urlparse(urltoscan)
        qwer = parsedurl.netloc.split('/')[2].split(':')[0]
        if qwer in listofdomains:
            return True
        else:
            return False

    def filtermessage(self,attachment):
        if (attachment.url != None):
            if (attachment.filename.endswith(".jpg" or ".png" or ".gif")):
                if (checkurlagainstdomain(attachment.url, domainlist)):
                    return True

class DiscordAuth(requests.auth.AuthBase):
    def __cls__(cls,self):
        self.discord_bot_token   = "NzE0NjA3NTAyOTg1MDAzMDgw.XxV-HQ.mn5f97TDYXtuFVgTwUccfsW4Guk"
    def __init__(self):
        self.discord_bot_token   = ""

    def __call__(self, r):
        return self.discord_bot_token



class APIRequest():
    '''uses Requests to return specific routes from a base API url'''
    def __init__(self, apibaseurl:str, thing:str):
        self.request_url = requote_uri("".format(apibaseurl,self.thing))
        blueprint("[+] Requesting: " + makered(self.request_url) + "\n")
        self.request_return = requests.get(self.request_url)


###############################################################################
#                MAIN CONTROL FLOW
###############################################################################
try:
    if __name__ == '__main__':
        try:
            bot.run(discord_bot_token, bot=True)
            if os.path.exists('./messagedatabase.db') == False:
                try:
                    DiscordMsgDB.create_all()
                    DiscordMsgDB.session.commit()
                    info_message("[+] Database Tables Created")
                except Exception:
                    errormessage("[-] Database Table Creation FAILED \n")
                try:
                    test_msg = DiscordMessage(sender = 'sender',
                                    time = 'time',
                                    content = 'content',
                                    file = 'file location, relative'
                                    )
                    addmsgtodb(test_msg)
                    info_message("[+] Test Commit SUCESSFUL, Continuing!\n")
                except Exception:
                    errormessage("[-] Test Commit FAILED \n") 
                try:
                    messagescraper = ScrapeChannel(channel,history_length)
                    messagescraper.dothethingjulie()
                except Exception:
                    errormessage("[-] Database Table Creation FAILED \n")
            else:
                warning_message('[+] Database already exists, skipping creation')
        except Exception:
            errormessage("[-] Database existence Check FAILED")
    else:
        print("wat")
except:
    redprint("[-] Error starting program")

