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
__description__ = '''Saves Discord Conversations per channel in sqlite3.db or csv.txt with images as base64.txt or png
'''

__docs__ = '''goto the following website and create a bot application. 
    You need to copy the token and user id

1. visit : https://discord.com/developers/applications

2. Click "create New Application", name it

3. on the left side, click "bot" and then click "build a bot"

4. Click "click to reveal your token "

5. copy that token to the config.cfg file

6. Permissions : 74752 is a reasonable default 
    but you can choose "8" for full control
    if you want to hack this bot to make more stuff

    Set that in the config.cfg file

7. 


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
def displaydocs(docs = docslist):
    '''Prints out the documentation'''
    for each in docslist:
        print(each)