from market_api.cyptowat import cyptowat
import json

api = cyptowat()

def ticker_list():
    res = api.get_ticker_list()

    if res['result_code'] != 0:
        return {'N/A'}
    else:
        return res['result_info']['result']
    
def ohlc(market, product, periods):
    res = api.get_ohlc(market, product, periods)

    if res['result_code'] != 0:
        return {'N/A'}
    else:
        return res['result_info']['result'][str(periods)]