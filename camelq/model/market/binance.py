from market_api.binance import binance
import json

api = binance()

def ticker(product):
    res = api.get_ticker(product)
    if res['result_code'] != 0:
        return {'N/A'}
    else:
        return {'market' : 'binance', 'product' : product,'price' : res['result_info']['price']}