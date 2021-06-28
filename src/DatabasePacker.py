
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
import pandas

from src.util import redprint,blueprint,greenprint,warning_message,errormessage
from src.database import DiscordMsgDB,DiscordMessage,addmsgtodb
###############################################################################
#                CHANNEL SCRAPING CLASS
###############################################################################
class DatabasePacker():
    def __init__(self):#,channel,server):
        #self.channel = channel
        #self.server = server
        self.filterfield = ""
        self.filterstring = ""

    def channelscrapetodb(self,dataframe:pandas.DataFrame):#,thing_to_get):
        try:
            #entrypoint for data
            dataframe.columns = ['channel','time','sender','content','file']
            # defaults to discarding empties... there are no empties
            if dataframe[self.filterfield] == self.filterstring:
                warning_message("[-] PANDAS - input : {} : discarded from rows".format(dataframe[self.filterstring]))
            else :                          #sender of message
                messagesent = DiscordMessage(channel = dataframe['channel'],
                                            time = dataframe['time'],
                                            sender = dataframe['sender'],
                                            content = dataframe['content'],
                                            # either a file path or base64 
                                            file = dataframe['file'])
                #push to DB
                addmsgtodb(messagesent)
        except Exception:
            errormessage("[-] DatabasePacker() FAILED")


greenprint("[+] Loaded Discord commands")
