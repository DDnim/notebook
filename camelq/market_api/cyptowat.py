import requests
import datetime
import hashlib, hmac, json
from common import *

class cyptowat():
    def __init__(self, key='', secret=b'', entry='https://api.cryptowat.ch/'):
        self.entry = entry
        self.key = key
        self.secret = secret

    def get_ticker_list(self):
        '''Get ticker list.'''
        response = requests.get(self.entry + 'markets/prices')
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))

    def get_ohlc(self, market, product, periods):
        '''Get ticker list.'''
        response = requests.get(self.entry + 'markets/' + market + '/' + product + '/ohlc?' + periods)
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))
