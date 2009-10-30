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

import logging
import sys
import re

__author__  = "Dolly Aswin Harahap <dolly.aswin@gmail.com>"
__status__  = "development"
__version__ = "0.10.09"
__date__    = "25 October 2009"

class Recharge:
    """
    Handle recharge 
    """

    LIMIT_RECORDS_IN_ONE_PAGE = 50.0

    # {{{ __init__(page) 
    def __init__(self, page):
        self._page = page
    # }}}

    # {{{ total() 
    def total(self):
        """
        fetch total records
        """
        pattern = re.compile("<strong>Total records : (\d+), .*</strong>", re.DOTALL)
        total = pattern.search(self._page)

        if total == None:
            return 0

        return float(total.group(1))
    # }}}

    # {{{ _getRecords() 
    def _getRecords(self):
        """
        fetch all records
        """
        pattern = re.compile("class=\"generic\">(.*)</table>[\n\t ]*<a", re.DOTALL)
        table = pattern.search(self._page)
        
        if table == None:
            # log here
            sys.exit()

        # split records
        records = re.split("</tr>[\n ]*", table.group(1))
        return records
    # }}}
        
    # {{{ getRows() 
    def getRows(self):
        """
        save all records to list
        """
        rows = []
        data = self._getRecords()

        for i,str in enumerate(data):
            # if empty string
            if len(str) < 1 or i == 0:
                continue
	
            pattern = re.compile(">([A-Za-z0-9\-: ]+)</", re.DOTALL)
            fields  = pattern.findall(str)
            rows.append(fields)

        if len(rows) == 0:
            return None

        return rows	
    # }}}

# vim: set ts=4 sw=4 tw=80 fdm=marker expandtab cin nohls:
