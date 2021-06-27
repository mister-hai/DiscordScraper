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

import PIL
import base64
import sys,os
from io import BytesIO
from util import redprint,blueprint,greenprint,warning_message,errormessage
###############################################################################
#                IMAGE SAVING CLASS
###############################################################################
randomimagename = lambda string: str(os.urandom(12)) + ".png"
class SaveDiscordImage():
    def __init__(self,  
                 imagebytes:bytes,
                 base64orfile = "file", 
                 filename = "",
                 imagesaveformat = ".png"):
        try:
            self.imagesaveformat = imagesaveformat
            self.imagein = imagebytes
            self.imageout = bytes

            if len(filename) > 0 :
                self.filename = filename
            else:
                self.filename = randomimagename
            self.image_as_base64 = base64orfile
            #they want to return a file blob
            if self.image_as_base64 == "file":
                try:
                    self.filename    = filename
                    greenprint("[+] Saving image as {}".format(self.filename))
                    self.image_storage = PIL.Image.open(self.imagein)
                    self.image_storage.save(self.filename, format = self.imagesaveformat)
                    self.image_storage.close()
                except Exception:
                    errormessage("[-] Exception when opening or writing Image File")
            #they want to return a text blob
            elif self.image_as_base64 == "base64" :
                buff = BytesIO()
                imagebytes.save(buff, format=self.imagesaveformat)
                self.image_storage = base64.b64encode(buff.getvalue())
                #self.image_storage = self.encode_image_to_base64(self.image_storage)
            else:
                raise ValueError
        except:
            errormessage("[-] Error with Class Variable self.base64_save")

    def imagedata(self):
        '''returns either base64 encoded text or a filebyte blob'''
        return self.image_storage
