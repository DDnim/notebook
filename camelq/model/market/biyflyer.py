from market_api.bitflyer import bitflyer
import json

api = bitflyer()

def ticker(product):
    res = api.get_ticker(product)
    if res['result_code'] != 0:
        return {'N/A'}
    else:
        return {'market' : 'bitflyer', 'product' : product,'price' : res['result_info']['ltp']}