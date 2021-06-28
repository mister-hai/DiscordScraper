
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
class DiscordScrape():
    def __init__(self,message):
        #if attachment exists in message
        if len(message.attachments) > 0:
            #process attachments to grab images
            for attachment in message.attachments:
                #its a link to something and that link is an image in 
                # discords CDN
                #TODO:
                # imgur
                # rule34
                # furaffinity
                # other furry shit
                if msghandler.filterattachment(attachment):
                    imagedata = msghandler.grabimage(discord_bot_token,attachment.url)
                    # we now have either base64 image data, or binary image data
                    # save the image to specific folder, accordin to date time
                    # making a new folder if we have to.
                    #base64 specific stuff
                        #gzip compression?
                    if arguments.saveformat == "base64":
                        imagedata = base64.b64encode(imagedata)
                    # if they want to save an image as a file and link to it in the database
                        #no gzip compression!
                    if arguments.saveformat == "file":
                        filepath = msghandler.savefile(imagedata, attachment.filename)
                        #now we change the image data to a file path of the image
                        imagedata = filepath
                else:
                    raise Exception
            #now we pack info into dataframe
            data = data.append({'channel'      : msg.channel,
                                'sender'       : msg.author.name,
                                'time'         : msg.created_at,
                                'content'      : msg.content,
                                'file'         : imagedata},
                                ignore_index = True)
            #perform data output
            msghandler.savemessageinloop(message= message)
        #stop at message limit
        if len(data) == limit:
            break

class DatabasePacker(DiscordScrape):
    def __init__(self):#,channel,server):
        #self.channel = channel
        #self.server = server
        self.filterfield = ""
        self.filterstring = ""


    def packframetodb(self,dataframe:pandas.DataFrame):#,thing_to_get):
        try:
            #inside the door for the entrypoint for data
            # defaults to discarding empties... there are no empties
            if dataframe[self.filterfield] == self.filterstring:
                warning_message("[-] PANDAS - input : {} : discarded from rows".format(dataframe[self.filterstring]))
            else :
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

