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
import gzip,io
import sys,os
import logging
import pkgutil
import inspect
import hashlib
import traceback
from pathlib import Path
from datetime import date
from os import _exit as exit
from signal import SIGINT, signal

TESTING = True
################################################################################
# Terminal Colorication Imports
################################################################################

try:
    import colorama
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    if TESTING == True:
        COLORMEQUALIFIED = True
except ImportError as derp:
    print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE, Install the Colorama Package from pip")
    COLORMEQUALIFIED = False

print("[+] Basic imports completed")

###############################################################################
#   LOGGING
################################################################  ###############
log_file            = 'LOGGING LOGGER LOG'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger              = logging.getLogger()
script_cwd          = Path().absolute()
script_osdir        = Path(__file__).parent.absolute()
###############################################################################
#   Lambdas
###############################################################################
redprint          = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
blueprint         = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint        = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
yellowboldprint = lambda text: print(Fore.YELLOW + Style.BRIGHT + ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
makeyellow        = lambda text: Fore.YELLOW + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else text
makered           = lambda text: Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen         = lambda text: Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue          = lambda text: Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
debugmessage     = lambda message: logger.debug(blueprint(message)) 
info_message      = lambda message: logger.info(greenprint(message))   
warning_message   = lambda message: logger.warning(yellowboldprint(message)) 
error_message     = lambda message: logger.error(redprint(message)) 
critical_message  = lambda message: logger.critical(yellowboldprint(message))
 
gzcompress = lambda inputdata: {"data" : gzip.compress(inputdata)}

scanfilesbyextension = lambda directory,extension: [f for f in os.listdir(directory) if f.endswith(extension)]

randomimagename = lambda string: str(os.urandom(12)) + ".png"

testurl = 'http://www.cwi.nl:80/%7Eguido/Python.html'

domainlist = ['discordapp.com', 'discord.com', "discordapp.net"]

defaultheaders = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   discord/0.0.309 Chrome/83.0.4103.122 \
                   Electron/9.3.5 Safari/537.36"}

greenprint("[+] Variables Set!")
################################################################################
##############                      Image                     #################
################################################################################

def saveimage(imageblob, filename, imagesaveformat):
    '''saves file as png,jpg, etc'''
    import PIL
    greenprint("[+] Saving image as {}".format(filename))
    try:
        image_storage = PIL.Image.open(imageblob)
        image_storage.save(filename, imagesaveformat)
        image_storage.close()
        greenprint("[+] Image Saved")
    except:
        errormessage("[-] Could Not Save Image with PIL")

################################################################################
##############                      SYSTEM                     #################
################################################################################
def errormessage(message):
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    try:
        error( message + ''.join(trace.format_exception_only()))
        #traceback.format_list(trace.extract_tb(trace)[-1:])[-1]
        blueprint('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    except Exception:
        error("EXCEPTION IN ERROR HANDLER!!!")
        redprint(message + ''.join(trace.format_exception_only()))

def sigintEvent(sig, frame):
    print('You pressed CTRL + C')
    exit(0)
signal(SIGINT, sigintEvent)

def error(message):
    # Append our message with a newline character.
    redprint('[ERROR]: {0}\n'.format(message))
    # Halt the script right here, do not continue running the script after this point.
    exit(1)

def warn(message):
    """Throw a warning message without halting the script.
    :param message: A string that will be printed out to STDERR.
    """
    # Append our message with a newline character.
    yellowboldprint('[WARN] {0}\n'.format(message))

def gzfilewritestring(datablob,filename):
    with gzip.open(filename, 'wb') as output:
        # We cannot directly write Python objects like strings!
        # We must first convert them into a bytes format using 
        # io.BytesIO() and then write it
        # CHECK TO MAKE SURE ITS A TYPE YOU CAN USE
        if type(datablob) in [str,list,dict]:
            with io.TextIOWrapper(output, encoding='utf-8') as encode:
                encode.write(datablob)
            
            byteswritten = "[+] {} Bytes Written to : {}".format(os.stat(filename).st_size, filename)
            greenprint(byteswritten)
        else:
            raise ValueError

def gzipreadfiletostring(filename, metaclassforfile):
    with gzip.open(filename, 'rb') as ip:
        with io.TextIOWrapper(ip, encoding='utf-8') as decoder:
            content = decoder.read()
            return content 


def md5(bytearray:bytes):
    ''' returns a sha512 digest of a password after salting with PBKDF'''
    herp = hashlib.md5()
    herp.update(bytearray)
    return herp.digest()

def sha256(bytearray:bytes,encoding =  "utf-8"):
    ''' returns a sha256 digest of a password after salting with PBKDF'''
    herp = hashlib.sha256()
    herp.update(bytearray)
    return herp.digest()

def sha512(bytearray:bytes,encoding =  "utf-8"):
    ''' returns a sha512 digest of a password after salting with PBKDF'''
    herp = hashlib.sha512()
    herp.update(bytearray)
    return herp.digest()