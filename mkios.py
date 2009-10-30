import mkios
import mkios.inventory
import mkios.recharge
import math
import sys
from optparse import OptionParser
from datetime import date

__version__ = '0.10.09'

url = {'recharge' : 'http://mkios.telkomsel.com/mkios/index.php?do=querytrx.recharge_own&post=1&',
       'inventory': 'http://mkios.telkomsel.com/mkios/index.php?do=info.inventory_own',
       'index' : 'http://mkios.telkomsel.com/mkios/index.php',
       'login' : 'http://mkios.telkomsel.com/mkios/index.php?do=common.login',
       'logout': 'http://mkios.telkomsel.com/mkios/index.php?do=common.logout'}

# {{{ parser options 
optp = OptionParser(usage="%prog -u USERNAME -p PIN [-a ACTION [-d DATE]]",
                    version="%prog " + __version__)
optp.add_option("-u", "--username", dest="username",
                help="msisdn mkios")
optp.add_option("-p", "--pin", dest="pin",
                help="pin mkios")
optp.add_option("-d", "--date", dest="date",
                default=date.today().strftime('%d-%m-%Y'),
                help="date of transaction")
optp.add_option("-a", "--action", dest="action",
		default="inventory",
		help="action")
(options, args) = optp.parse_args()

if options.username == None or options.pin == None:
    optp.error("Username and Pin required")
# }}}

# reverse date
revdate = '-'.join(options.date.split('-')[::-1])
# create cookie
opener  = mkios.setOpener()
index = mkios.grab(opener, url['index'])
# login
login = mkios.Login(opener, index.read(), url['login'],
                    options.username, options.pin)

# check url location
if (login.opener.geturl() == url['login']):
    # change stderr to log
    sys.stderr.write('Invalid MSISDN or PIN\n')
    sys.exit()

# switch action
if options.action == "inventory":
    # inventory
    inventory = mkios.inventory.Inventory(mkios.grab(opener, url['inventory']).read())
    mkios.save(mkios.filename(options.action, options.username, revdate),
               inventory.getRows())
elif options.action == "recharge":
    # fetch page 1 first
    recharge_url = url['recharge'] + 'date=' + options.date + '&page=' + '1'
    recharge = mkios.recharge.Recharge(mkios.grab(opener, recharge_url).read())
    # save all records 
    mkios.save(mkios.filename(options.action, options.username, revdate),
               recharge.getRows())
    # get total records
    total_page = math.ceil(recharge.total() / recharge.LIMIT_RECORDS_IN_ONE_PAGE)
    # start loop from page 2
    page = 2

    while (page <= total_page):
        # fetch page
        recharge_url = url['recharge'] + 'date=' + options.date + '&page=' + str(page)
        recharge = mkios.recharge.Recharge(mkios.grab(opener, recharge_url).read())
        # save all records 
        mkios.save(mkios.filename(options.action, options.username, revdate),
                   recharge.getRows())
        # increment page
        page += 1

# vim: set ts=4 sw=4 tw=80 fdm=marker expandtab cin nohls:
