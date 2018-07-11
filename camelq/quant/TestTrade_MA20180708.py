from market_api import cyptowat
from market_api import bitflyer
import pandas
import talib
import numpy as np
import time

def get_positions(pf):
    if pf.empty:
        return 0
    elif pf['side'][0] == 'BUY':
        return pf['size'].sum()
    else:
        return - pf['size'].sum()
    

class quant():
    def __init__(self, setting):
        self.setting = setting
        self.data_api = cyptowat.cyptowat()
        self.trade_api = bitflyer.bitflyer(setting['market0']['key'], setting['market0']['secret'])

    def refresh_data(self):
        s = self.setting
        self.ohlc = self.data_api.get_ohlc(s['market0']['name'], s['market0']['products']['set0']['product0']['data'], '180')
        self.ticker = self.trade_api.get_ticker(s['market0']['products']['set0']['product0']['name'])

    def run(self):
        while True:
            try:
                self.refresh_data()
                self.ohlc['result_info']
                pf = pandas.DataFrame(self.ohlc['result_info'], columns=["time", "open", "close", "high", "low", "size","value"])
                pf['time'] = pandas.to_datetime(pf['time'],unit='s')
                i = pf['close']

                MA5 = talib.MA(np.array(i, dtype='f8'), timeperiod=100)
                MA20 = talib.MA(np.array(i, dtype='f8'), timeperiod=400)
                
                ma5i = np.array(MA5)[-1]
                ma20i = np.array(MA20)[-1]
                positions = pandas.read_json(self.trade_api.get_positions('FX_BTC_JPY')['result_info'])
                print(positions)
                positions_sum = get_positions(positions)
                
                if ma5i > ma20i:
                    if positions_sum < 0.02:
                        self.trade_api.request_order('FX_BTC_JPY', 'BUY', 0, 0.01)
                elif ma5i <= ma20i:
                    if positions_sum > 0.02:
                        self.trade_api.request_order('FX_BTC_JPY', 'SELL', 0, 0.01)
                time.sleep(30)
            except:
                time.sleep(30)