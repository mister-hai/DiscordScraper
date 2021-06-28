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
import sys,os
import inspect
import traceback
from datetime import date


###############################################################################
#                Flask Server / Flask Routes / User Interface
###############################################################################
#from sqlalchemy import inspect

import flask
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from flask import Flask, render_template, Response, Request ,Config

from util import redprint,blueprint,greenprint,warning_message,errormessage
from util import makered,info_message
################################################################################
##############                      CONFIG                     #################
################################################################################
TESTING = True
#TEST_DB            = 'sqlite://'
DATABASE           = "discordmessages"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + ".db"
DATABASE_FILENAME  = DATABASE + '.db'

if database_exists(LOCAL_CACHE_FILE) or os.path.exists(DATABASE_FILENAME):
    DATABASE_EXISTS = True
else:
    DATABASE_EXISTS = False        
  
class Config(object):
# TESTING = True
# set in the std_imports for a global TESTING at top level scope
    SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = False

try:
    engine = create_engine(LOCAL_CACHE_FILE , connect_args={"check_same_thread": False},poolclass=StaticPool)
    PybashyDatabase = Flask(__name__ )
    PybashyDatabase.config.from_object(Config)
    DiscordMsgDB = SQLAlchemy(PybashyDatabase)
    DiscordMsgDB.init_app(PybashyDatabase)
    if TESTING == True:
        DiscordMsgDB.metadata.clear()
except Exception:
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    errormessage("[-] Database Initialization FAILED \n" + ''.join(tb.format_exception_only()))

###############################################################################
#                DATABASE MODELS
###############################################################################

class DiscordMessage(DiscordMsgDB.Model):
    __tablename__       = 'Messages'
    #__table_args__      = {'extend_existing': True}
    id       = DiscordMsgDB.Column(DiscordMsgDB.Integer,
                           index         = True,
                           unique        = True,
                           autoincrement = True)
    channel   = DiscordMsgDB.Column(DiscordMsgDB.String(256), primary_key   = True)
    time      = DiscordMsgDB.Column(DiscordMsgDB.String(64))
    sender    = DiscordMsgDB.Column(DiscordMsgDB.string(64))
    content   = DiscordMsgDB.Column(DiscordMsgDB.Text)
    #filelocation or base64
    file      = DiscordMsgDB.Column(DiscordMsgDB.Text)
    originalfileurl = DiscordMsgDB.Column(DiscordMsgDB(256))
    def __repr__(self):
        return '''=========================================
channel : {}
sender : {} 
time : {} 
message : {} 
'''.format(self.channel,
            self.sender,
            self.time,
            self.message
        )

###############################################################################
###             DATABASE FUNCTIONS
#########################################################
def add_to_db(thingie):
    """
    Takes SQLAchemy model Objects 
    For updating changes to Class_model.Attribute using the form:
        Class_model.Attribute = some_var 
        add_to_db(some_var)
    """
    try:
        DiscordMsgDB.session.add(thingie)
        DiscordMsgDB.session.commit
        redprint("=========Database Commit=======")
        greenprint(thingie)
        redprint("=========Database Commit=======")
    except Exception as derp:
        print(derp)
        print(makered("[-] add_to_db() FAILED"))

def ReturnMessageVar(message, var):
    return message.query.filter_by(var)

def ReturnMessageById(idnum):
    DiscordMsgDB.session.query(idnum)

def querychannelall(channelname):
    DiscordMsgDB.session.query(DiscordMessage).filter_by(channel = channelname)

def addmsgtodb(msg_to_add):
    """
    "name" is the primary key of DB, is unique
    """
    try:
        if DiscordMsgDB.session.query(msg_to_add).filter_by(name=msg_to_add.name).scalar() is not None:
            info_message('[+] Duplicate Entry Avoided : ' + msg_to_add.sender + " : " + msg_to_add.time)
        # and doesnt get added
        else: # and it does if it doesnt... which works out somehow ;p
            DiscordMsgDB.session.add(msg_to_add)
            info_message('[+] Message Added To Database : ' + msg_to_add.sender + " : " + msg_to_add.time)
    except Exception:
        errormessage("[-] addmsgtodb() FAILED")

def update_db():
    try:
        DiscordMsgDB.session.commit()
    except Exception as derp:
        print(derp.with_traceback)
        print(makered("[-] Update_db FAILED"))


def doesexistbyID(plant_name):
    try:
        exists = DiscordMsgDB.session.query(DiscordMessage.id) is not None
    except Exception:
        errormessage('[-] Database VERIFICATION FAILED!')
    if exists:
        info_message("[-] Message already in database... Skipping!")
        return True
    else:
        return False

def does_exists(self,Table, Row):
    try:
        if DiscordMsgDB.session.query(Table.id).filter_by(name=Row).first() is not None:
            info_message('[+] MESSAGE {} Exists'.format(Row))
            return True
        else:
            return False        
    except Exception:
        errormessage('[-] Database VERIFICATION FAILED!')

def table_exists(name):
    try:
        from sqlalchemy import inspect
        blarf = inspect(engine).dialect.has_table(engine.connect(),name)
        if blarf:
            info_message('[+] Database Table {} EXISTS'.format(name))
            return True
        else:
            return False
    except Exception:
        errormessage("[-] TABLE {} does NOT EXIST!".format(name))
        return False

greenprint("[+] Database functions loaded!")