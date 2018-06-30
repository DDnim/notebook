import indicator.bitflyer as bf
import pandas

import numpy as np
import talib
import matplotlib.pyplot as plt

from account.account import account
from market_api.research_server import research
import database.bitflyer as db
import datetime,time

a = account()
a.balance = 30000000

server = research(a)
server.set_lantecy = 200

b = bf.indicator_bitflyer('BTC_JPY')
d = b.get_ohlc('2018-01-01 00:00:00', '2018-05-02 00:00:00')

MA5 = talib.MA(np.array(d['close']), timeperiod=5)
MA20 = talib.MA(np.array(d['close']), timeperiod=20)
p_p = 0
v=[]

plt.plot(np.array(d.index),MA5)
plt.pause(.01)
unix_time = int(time.mktime(d.index[1].timetuple()))
profit = float(server.get_tick('BTC_JPY',unix_time)['price'])
scale = profit
a.balance = server.get_balance()
for i in range(0, len(d)):
    if MA5[i] < MA20[i]:
        if a.balance > 10000000:
            unix_time = int(time.mktime(d.index[i+1].timetuple()))
            p_c = float(server.get_tick('BTC_JPY',unix_time)['price'])
            p_p = int(a.balance/p_c)
            print(d.index[i], a.balance , p_c, p_p)
            profit = a.balance
            server.order(side = 'buy', product = 'BTC_JPY', size = p_p, price = 0, time = unix_time)
            a.balance = server.get_balance()
            #print(server.get_executions())
    else:
        if a.balance <= 10000000:
            unix_time = int(time.mktime(d.index[i+1].timetuple()))
            p_c = float(server.get_tick('BTC_JPY',unix_time)['price'])
            print(d.index[i], a.balance + p_p * p_c, p_c,p_p)
            profit = a.balance + p_p * p_c
            #p_p = a.stock_list['BTC_JPY'].size
            server.order(side = 'sell', product = 'BTC_JPY', size = p_p, price = 0, time = unix_time)
            a.balance = server.get_balance()
    if i % 1000 == 0:
        plt.plot(d.index[i], profit * scale / 30000000,'.')
        plt.pause(.01)

plt.show()