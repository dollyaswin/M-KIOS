# Copyright 2009 by Dolly Aswin Harahap <dolly.aswin@gmail.com>
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Dolly Aswin Harahap
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# DOLLY ASWIN HARAHAP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# DOLLY ASWIN HARAHAP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE

"""
Mkios package for python

Copyright (C) 2009 Dolly Aswin Harahap. All Rights Reserved.
"""

__all__ = ['Login', 'Inventory', 'Recharge']

import cookielib
import logging
import urllib2
import hashlib
import urllib
import sys
import csv
import os
import re

__author__  = "Dolly Aswin Harahap <dolly.aswin@gmail.com>"
__status__  = "development"
__version__ = "0.10.09"
__date__    = "25 October 2009"

# {{{ setOpener() 
def setOpener():
    """
	Return opener
	"""

    cj = cookielib.CookieJar()
    op = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    op.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US;' +
                      'rv:1.9.0.1) Gecko/2008070206 Firefox/3.0.1')]
    
    return op
# }}}

# {{{ grab(opener, url, data = None) 
def grab(opener, url, data = None):
	"""
	Return object
	"""
	
	try:
		fetch = opener.open(url, data)
	except:
		exception = sys.exc_info()
		sys.stderr.write('%s : %s \n' % (exception[0], exception[1]))
		sys.exit()
	
	return fetch
# }}}

# {{{ filename(type, username, date) 
def filename(type, username, date):
	"""
	Return file name
	"""
	
	try:
		os.mkdir(type)
	except OSError:
		pass

	return type + '/' + date + '-' + username + '.csv'	
# }}}

# {{{ save(filename, rows) 
def save(filename, rows):
	"""
	Save list into csv file
	"""

	csvwriter = csv.writer(open(filename, 'a'))
	csvwriter.writerows(rows)
# }}}

class Login:
    """
    Handle login 
    """

    opener = None

    def __init__(self, opener, page, url, username, pin):
        self._username = username
        self._opener = opener
        self._page = page
        self._url  = url
        self._pin  = pin
        self.opener  = self.do()
        
    def _fetchChallenge(self):
        """
        Return challenge key on page
        """
        pattern = re.compile("\"challenge\" value=\"([\w]+)\"", re.DOTALL)
        
        try:
            challenge = pattern.search(self._page).group(1)
        except AttributeError:
            sys.stderr.write('Challenge not match\n')
            sys.exit()
        
        return challenge

    def do(self):
        """
        Login
        """
        challenge = self._fetchChallenge()
        md5  = hashlib.md5()
        md5.update(challenge + self._pin) 
        data = urllib.urlencode({'username' : self._username,
                                 'password' : md5.hexdigest(),
                                 'challenge': challenge})
        return grab(self._opener, self._url, data)

# vim: set ts=4 sw=4 tw=80 fdm=marker expandtab cin nohls:
