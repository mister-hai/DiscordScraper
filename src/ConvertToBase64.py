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
Converts an image to base 64 and saves it if desired
"""

import PIL
import base64
import sys,os
from io import BytesIO
from src.util import redprint,blueprint,greenprint,warning_message,errormessage
###############################################################################
#                IMAGE SAVING CLASS
###############################################################################
class ImageToBase64():
    '''specifically for the operation of:
    - converting image data to base64
    - saving images
if image name is empty, makes a random 12 ints
'''
    def __init__(self,imagebytes:bytes,imagesaveformat:str)-> None:
        #DOWNLOAD THE IMAGE
        self.imagein = imagebytes
        self.imageout = bytes
        self.imagesaveformat = imagesaveformat
        #they want to return a text blob
        self.converttobase64(imagebytes = self.imagein)
        self.imagedata()

    def converttobase64(self, imagebytes):
        buff = BytesIO()
        imagebytes.save(buff, format=self.imagesaveformat)
        self.image_storage = base64.b64encode(buff.getvalue())
        #self.image_storage = self.encode_image_to_base64(self.image_storage)

    def imagedata(self):
        '''returns base64 encoded text'''
        return self.image_storage
