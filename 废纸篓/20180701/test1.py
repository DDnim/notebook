import indicator.bitflyer as bf
import pandas
import datetime

import numpy as np
import talib
import matplotlib.pyplot as plt



print(datetime.datetime(2018, 5, 1, 23, 46).timestamp())

b = bf.indicator_bitflyer('BTC_JPY')

d = b.get_ohlc('2018-04-01 00:00:00', '2018-05-02 00:00:00')

MA5 = talib.MA(np.array(d['close']), timeperiod=5)
MA20 = talib.MA(np.array(d['close']), timeperiod=20)

c = 100000000
p = 1
v = []
for i in range(0, len(d)):
    if MA5[i] > MA20[i]:
        if c > 0:
            p = c/d['close'][i]
            c = 0
        v.append(p * d['close'][i])
    else:
        if p > 0:
            c = p * d['close'][i]
            p = 0
        v.append(c)


print(v)
plt.plot(np.array(d.index),v,'*')
plt.plot(np.array(d.index),MA5)

plt.show()