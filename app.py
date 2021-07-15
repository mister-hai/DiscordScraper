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
__prog__ = """
Discord bot Tied to Code Performing Message Archival
"""
################################################################################
# Imports
################################################################################
print("[+] Starting Discord Scraping Utility")
TESTING = True
import gzip
import sys,os
from datetime import datetime,date


from docs import *
from commands import *
from src.util import redprint,blueprint,greenprint,errormessage,debugmessage
from src.util import warn,yellowboldprint,warning_message,scanfilesbyextension
from src.util import info_message,gzfilewritestring,gzcompress,gzipreadfiletostring
from src.database import table_exists,dbtest

greenprint("[+] Modules Imported")
################################################################################
# Variables, Technically "loose ends", the dangly bits that you connect to 
# other code that functionally represent the ends of wires/data pipelines/etc...
################################################################################
global timeofrun
global today
today = date.today()
timeofrun = datetime.now()
attachmentsurl = "/attachments/"
#filterfordiscorddomain = lambda string: for domain in string[0:26] if  # == "https://cnd.discordapp.com"
#token   = "NzE0NjA3NTAyOTg1MDAzMDgw.XxV-HQ.mn5f97TDYXtuFVgTwUccfsW4Guk"

greenprint("[+] Global Variables Set")
###############################################################################
#                        Command Line Arguments
###############################################################################
import argparse
import configparser

parser = argparse.ArgumentParser(
    prog=__prog__,
    description='Discord Message Archival',
    epilog="RUNNING THIS PROGRAM WITH THE --token EMPTY WILL FORCE IT TO USE THE CONFIG FILE",
    )
    #860037305368838164
#parser.add_argument('--user',
#                                 dest    = 'user',
#                                 action  = "store" ,
#                                 default = "860037305368838164", 
#                                 help    = "FUTURE OPTION: discord bot USER ID for O-Auth process" )
#parser.add_argument('--secret',
#                                 dest    = 'user',
#                                 action  = "store" ,
#                                 default = "8h_n6kg29RwFBKj6IHSdjHZL67EdV6NM", 
#                                 help    = "FUTURE OPTION: discord bot SECRET for O-Auth process" )
parser.add_argument('--auth-token',
                                dest    = 'token',
                                action  = "store" ,
                                default = "", 
                                help    = "discord bot TOKEN for BASIC BOT Auth process. \n\
        LEAVE EMPTY TO USE THE CONFIG FILE FOR ALL ARGUMENTS \n",
                                required = False)
parser.add_argument('--images',
                                dest    = 'images',
                                action  = "store_true",
                                default = False, 
                                help    = "set if images are saved AT ALL.\
                                    DEFAULT IS NO IMAGES SAVED",
                                required = False)
parser.add_argument('--messagelimit',
                                dest    = 'limit',
                                action  = "store" ,
                                default = "10000", 
                                help    = "Number of messages to download",
                                required = False)
parser.add_argument('--databasename',
                                dest    = 'dbname',
                                action  = "store" ,
                                default = "discordmessagehistory", 
                                help    = "Name of the file to save the database as",
                                required = False)
#parser.add_argument('--pandascolumns',
#                                dest    = 'pandascolumns',
#                                action  = "store" ,
#                                default = 'channel,sender,time,content,file', 
#                                help    = "dev option: message sections to archive, do not modify\
#                                    unless you know what you are doing",
#                                required = False)
#parser.add_argument('--saveascsv',
#                                dest    = 'saveascsv',
#                                action  = "store" ,
#                                default = False, 
#                                help    = "FUTURE OPTION: save messages as CSV file",
#                                required = False)
parser.add_argument('--imagesaveformat',
                                dest    = 'imagesaveformat',
                                action  = "store" ,
                                default = ".png", 
                                help    = "File extension for saving images",
                                required = False)
parser.add_argument('--gzipped',
                                dest    = 'gzipenabled',
                                action  = "store",
                                default = True, 
                                help    = "will gzip as much as possible to save space",
                                required = False)
parser.add_argument('--compressionfactor',
                                dest    = 'compressionfactor',
                                action  = "store",
                                default = 5, 
                                help    = "Sets compression factor for all GZIP \
                                    operations : integer 0-9 Default : 5",
                                required = False)
parser.add_argument('--docs',
                                dest    = 'printdocumentation',
                                action  = "store",
                                default = True, 
                                help    = "Prints the Documentation to the terminal, \
                                    use './app.py --docs >> docs.txt' to save to a file",
                                required = False) 
###############################################################################
##                     CONFIGURATION FILE PARSER                             ##
###############################################################################
try:
    arguments = parser.parse_args()
    if len(arguments.token) == 0:
        try:
            config              = configparser.ConfigParser()
            token               = config['DEFAULT']['token']
            dbname              = config['DEFAULT']['dbname']
            images              = config['DEFAULT']['images']
            gzipenabled         = config['DEFAULT']['gzipenabled']
            compressionfactor   = config['DEFAULT']['compressionfactor']
            domainlist          = config['DEFAULT']['domainlist'].split(",")
            listofpandascolumns = config['DEFAULT']['pandascolumns'].split(",")
        except Exception:
            errormessage("[-] Configuation File could not be parsed!")
            sys.exit(1)
    elif len(arguments.token) == 59:
        if arguments.gzipenabled:
            gzipcompressionfactor = arguments.compressionfactor
        token = arguments.token
        dbname = arguments.dbname
        images = arguments.images
        domainlist = arguments.domainlist.split(",")
        listofpandascolumns = arguments.listofpandascolumns.split(',')
except Exception:
    errormessage("[-] CommandLine Arguments Could Not Be Parsed!")
    sys.exit(1)
greenprint("[+] Loaded Commandline Arguments")

###############################################################################
#                MAIN CONTROL FLOW
###############################################################################
if __name__ == '__main__':
    try:
###############################################################################
#                TEST ON START
###############################################################################
        #check for database file
        
        greenprint("[+] Testing Database")
        if os.path.exists(dbname) == False:
            dbtest()
###############################################################################
#        DO THE THING JULIE! THE THING! DO IT!
###############################################################################
            # IMPORTANT!!!
            # IF database file already exists!
            # backup this db file, ONLY the file.db!!
            #   to an archive in BOTH this folder at the TLD, and the ~/DESKTOP/data.db~!
            ## ADD IMAGES TO ARCHIVE IN /images/ FOLDER
        elif os.path.exists(dbname) == True:
            greenprint("[+] Database File Exists!")
            yellowboldprint("[+] backing up db file before performing an operation on it!")
            # int 0-9
            with open(dbname) as databasefile:
                gzip.compress(databasefile,compresslevel=compressionfactor)
            #check for tables
            for each in listofpandascolumns:
                if table_exists(each):
                    warning_message('[+] Table : {} verified'.format(each))
                else:
                    raise Exception
###############################################################################                        
        #perform the actual activity requested by the user
        try:
            bot.run(token, bot=True)
        except Exception:
            errormessage("[-] BOT OPERATION FAILED!!! \n")
###############################################################################
    except Exception:
        redprint("[-] Error starting program")

