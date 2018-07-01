from account.account import account
from market_api.research_server import research
import database.bitflyer as db
import datetime,time

a = account()
a.balance = 30000000

server = research(a)
server.set_lantecy = 200

print(server.get_balance())

base_data = "Feb 27 00:51:29 2018 GMT"
date_time = time.strptime(base_data, "%b %d %H:%M:%S %Y GMT")
unix_time = int(time.mktime(date_time))

p_c = float(server.get_tick('BTC_JPY',unix_time)['price'])

server.order(side = 'buy', product = 'BTC_JPY', size = a.balance/p_c, price = 0, time = unix_time)
server.order(side = 'buy', product = 'BTC_JPY', size = 15, price = 0, time = unix_time)


