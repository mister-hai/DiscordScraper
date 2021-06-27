# -*- coding: utf-8 -*-
#!/usr/bin/env python
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
from distutils.core import setup

LONG_DESCRIPTION = '''
Discord Scraping Utility I made to save important conversations
'''        
    
setup(name = 'blorp a lot',
        version = '0.1',
        description = 'Statistical and Metrical Tooling for Crypto and Maths Lernin',
        long_description = LONG_DESCRIPTION,
        author = 'bitches stealing shit',
        author_email = 'mrhai_gmail.fuckyourself',
        url = 'https://github.com/mister-hai/CryptoLib',
        packages = ['CryptoLib'],
        classifiers = [
          'Topic :: Security :: Cryptography',
          'License :: OSI Approved :: WATtm License',
        ],
        dependency_links=[
          'http://github.com/user/repo/tarball/master#egg=package-1.0'
        ],
        install_requires=[
          'flask',
          'flask-sqlalchemy',
          'numpy'
        ],
        license = "License :: OSI Approved :: WATtm License",
    )
