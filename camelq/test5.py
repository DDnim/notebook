import model.indicator.bitflyer as bf
import pandas

import numpy as np
# from talib import abstract
import talib
import matplotlib.pyplot as plt

from model.account.account import account
from market_api.research_server import research
import database.bitflyer as db
import datetime,time

a = account()
a.balance = 30000000

server = research(a)
server.set_lantecy = 15

b = bf.indicator_bitflyer('BTC_JPY')
d = b.get_ohlc('2018-02-01 00:00:00', '2018-06-02 00:00:00')
d = d.asfreq('3MIN').ffill(limit=4)
# sma = abstract.Function('sma')
MA5 = talib.EMA(np.array(d['close'],dtype='f8'), timeperiod=100)
MA20 = talib.EMA(np.array(d['close'],dtype='f8'), timeperiod=400)
p_p = 0
v=[]

print(len(np.array(d['close'],dtype='f8')),len(np.array(d.index)),len(MA5),len(MA20))
print(np.array(d['close'],dtype='f8'),np.array(d.index),MA5,MA20)

plt.plot(np.array(d.index),MA5)
plt.plot(np.array(d.index),MA20)
# plt.show()


plt.pause(.01)
unix_time = int(time.mktime(d.index[1].timetuple()))
profit = float(server.get_tick('BTC_JPY',unix_time)['price'])
scale = profit
a.balance = server.get_balance()
p=[]
v=[]
for i in range(0, len(d)):
    a.balance = server.get_balance()
    if MA5[i] > MA20[i]:
        if a.balance > 10000000:
            unix_time = int(time.mktime(d.index[i+1].timetuple()))
            p_c = float(server.get_tick('BTC_JPY',unix_time)['price'])
            p_p = int(a.balance/p_c - a.balance/p_c * 0.0015)
            print('buy',d.index[i], a.balance , p_c, p_p)
            profit = a.balance
            server.order(side = 'buy', product = 'BTC_JPY', size = p_p, price = 0, time = unix_time)
    elif MA5[i] <= MA20[i]:
        if a.balance <= 10000000:
            unix_time = int(time.mktime(d.index[i+1].timetuple()))
            p_c = float(server.get_tick('BTC_JPY',unix_time)['price'])
            print('sell',d.index[i], a.balance + p_p * p_c, p_c,p_p)
            profit = a.balance + p_p * p_c
            server.order(side = 'sell', product = 'BTC_JPY', size = p_p, price = 0, time = unix_time)
    p.append(profit * scale / 30000000)
    if a.balance > 10000000:
        v.append(a.balance)
    else:
        v.append(a.balance + p_p * p_c)

plt.plot(np.array(d.index),v)
plt.plot(np.array(d.index),p)
plt.show()