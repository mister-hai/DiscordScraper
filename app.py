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
#                  DOCUMENTATION
################################################################################

"""
Discord bot message archival
"""
__description__ = '''
'''
__docs__ = '''
'''
__credits__ = {"credit1":"mister_hai",
                "credit2":"",
                "credit3":""}

__filestructure__ = """
/module/
    setup.py
    app.py
    --- IF SAVING AS SQLITE3DB ---
    DATABASE.DB IS HERE
        /src
            __init__.py
            src1.py
            src2.py
            src....py
        /database
            /images
                /channel1
                    /date-time
                        img1-date-time.jpg.b64
                        img2-date-time.jpg.b64
                        img3-date-time.jpg.b64
                /channel2
                    /date-time
                        img1-date-time.jpg.b64
                        img2-date-time.jpg.b64
                        img3-date-time.jpg.b64
                /channel3
                    /date-time
                        img1-date-time.jpg.b64
                        img2-date-time.jpg.b64
                        img3-date-time.jpg.b64
--- IF SAVING AS CSV ---
            /messages
                /channel1
                    msgset1-date-time.csv
                    msgset2-date-time.csv
                    msgset3-date-time.csv
                /channel2
                    msgset1-date-time.csv
                    msgset2-date-time.csv
                    msgset3-date-time.csv
                /channel3
                    msgset1-date-time.csv
                    msgset2-date-time.csv
                    msgset3-date-time.csv
--- MESSAGES ARE STORED BY CHANNEL--
--- AND SAVED AS ONE FILE PER RUN, PER CHANNEL---
"""
docslist = [__description__,__docs__,__credits__,__filestructure__]
def displaydocs(docslist):
    '''Prints out the documentation'''
    for each in docslist:
        print(each)
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
import shutil
###############################################################################
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
import discord
from discord.ext import commands, tasks
###############################################################################
from src.DatabasePacker import DatabasePacker
from src.HTTPRequest import HTTPDownloadRequest
from src.SaveDiscordImage import SaveDiscordImage
from src.database import DiscordMsgDB,DiscordMessage,addmsgtodb
from src.util import redprint,blueprint,greenprint,errormessage,debugmessage
from src.util import warn,yellowboldprint,warning_message,scanfilesbyextension
from src.util import info_message
from src.database import table_exists
################################################################################
# Variables, Technically "loose ends", the dangly bits that you connect to 
# other code that functionally represent the ends of wires/data pipelines/etc...
################################################################################
global timeofrun
global today
today = date.today()
timeofrun = datetime.now()

#setting defaults for use without argparse
imagesaveformat = ".png"

#an example of how to craft a bullshit filter to select only items of contextual value
fileextensionfilter = [".jpg",".png",".gif"]
#dataframe.columns = ['channel','time','sender','content','file']
listofpandascolumns = ['channel', 'sender', 'time', 'content','file']
domainlist = ['discordapp.com', 'discord.com', "discordapp.net", "imgur.com"]
porndomains = ["rule34.xxx"]
attachmentsurl = "/attachments/"
#filterfordiscorddomain = lambda string: for domain in string[0:26] if  # == "https://cnd.discordapp.com"
discord_bot_token   = "NzE0NjA3NTAyOTg1MDAzMDgw.XxV-HQ.mn5f97TDYXtuFVgTwUccfsW4Guk"
COMMAND_PREFIX      = "."
bot_help_message    = "I AM"
BOT_PERMISSIONS     = 3072
devs                = [712737412018733076]
#cog_directory_files = os.listdir("./cogs")
load_cogs           = False
bot = discord.Bot()
bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
client = discord.Client()
guild = discord.Guild
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
parser.add_argument('--auth-token',
                                 dest    = 'token',
                                 action  = "store" ,
                                 default = discord_bot_token, 
                                 help    = "string, no quotes, of your discord bot token.\
                                     No, this script is not going to steal it, Read the source" )
parser.add_argument('--gzipped',
                                 dest    = 'gzipenabled',
                                 action  = "store",
                                 default = True, 
                                 help    = "will gzip as much as possible to save space")    
arguments = parser.parse_args()

# need this here, in this spot
# mixing OOP and procedural programming paradigms
# to allow for a more customizable "shape"
if  arguments.saveformat == "csv":
    SAVETOCSV = True
else:
    SAVETOCSV == False

###############################################################################
#                DISCORD COMMANDS
###############################################################################
# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@bot.event
async def on_ready():
    print("Discrod Scraper ALPHA")
    await bot.change_presence(activity=discord.Game(name="yo mamma say .help"))
    #await lookup_bot.connect()

imagedirectory = os.getcwd() + "/images/"

#function to call the scraper class when ordered
@bot.command
async def scrapemessages(message,limit):
    #get the input
    dbpacker = DatabasePacker()
    msghandler= MessageHandler()
    #itterate over messages in channel until limit is reached
    for msg in message.channel.history(limit):
        # filter the messages to exlude various entities
        if msghandler.filtermessage(message=message):
            # colums defined at the top
            data = pandas.DataFrame(columns=listofpandascolumns)

greenprint("[+] Loaded Discord commands")

###############################################################################
#                MAIN CONTROL FLOW
###############################################################################

if __name__ == '__main__':
    try:
###############################################################################
        #check for database file
        if os.path.exists(arguments.dbname) == False:
            #if its not there, make file
            DiscordMsgDB.create_all()
            DiscordMsgDB.session.commit()
            info_message("[+] Database Tables Created")
            #test database entry mechanics
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
###############################################################################
            # IMPORTANT!!!
            #database file already exists!
            #backup this db file, ONLY the file.db!!
            ## ADD IMAGES TO ARCHIVE IN FOLDER
        elif os.path.exists(arguments.dbname) == True:
            greenprint("[+] Database File Exists!")
            #check for tables
            for each in listofpandascolumns:
                if table_exists(each):
                    warning_message('[+] Table : {} verified'.format(each))
                else:
                    raise Exception
###############################################################################                        
        #perform the actual activity requested by the user
        try:
            #start the bot
            bot.run(discord_bot_token, bot=True)
        except Exception:
            errormessage("[-] BOT OPERATION FAILED!!! \n")
###############################################################################
    except Exception:
        redprint("[-] Error starting program")

