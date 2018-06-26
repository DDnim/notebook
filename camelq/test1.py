import indicator.bitflyer as bf
import pandas
import datetime

print(datetime.datetime(2018, 5, 1, 23, 46).timestamp())

b = bf.indicator_bitflyer('BTC_JPY')

d = b.get_ohlc('2018-04-01 00:00:00', '2018-05-02 00:00:00')

for t in pandas.date_range(start = '2018-04-01 00:00:00', end = '2018-06-01 00:00:00', freq='1min'):
    s = t.timestamp()
    if s in d.keys():
        print(d[s])

#print(datetime.datetime('2018-04-01 00:00:00'))