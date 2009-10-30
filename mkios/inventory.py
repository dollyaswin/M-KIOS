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

class Inventory:
    """
    Handle fetch inventory 
    """

    # {{{ __init__(page) 
    def __init__(self, page):
        self._page = page
    # }}}

    # {{{ _getRecords() 
    def _getRecords(self):
        """
        fetch records
        """
        # fetch table 
        pattern = re.compile("(<strong>.*)(\n</div>\n</div>)", re.DOTALL)
        table = pattern.search(self._page)

        if table == None:
            # log here
            sys.exit()

        # fetch type
        # pattern = re.compile("<strong>([\w ]+)</strong>", re.DOTALL)
        # type = pattern.findall(table.group())
        #
        # if len(type) <= 0:
        #     type = ['', '']

        # fetch data in table
        pattern = re.compile("<tr>([\w</>\-\n ]+)</tr>", re.DOTALL)
        records = pattern.findall(table.group())

        if len(records) == None:
            return None

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
            std = re.compile("([\n ]*<td>|[\n ]*<tr>)", re.DOTALL).sub('', str)
            ctd = re.compile("(</td>[\n]*)", re.DOTALL).sub('\t', std)
            ntr = re.compile("(</tr>[\n]*)", re.DOTALL).sub('\n', ctd)
            [rows.append(notab.split('\t')) for notab in ntr.split('\n')]
            rows.append([])
        
        if len(rows) == 0:
            return None

        return rows	
    # }}}

# vim: set ts=4 sw=4 tw=80 fdm=marker expandtab cin nohls:
