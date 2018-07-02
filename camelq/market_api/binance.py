import requests
import datetime
import hashlib, hmac, json
from common import *

class binance():
    def __init__(self, key='', secret=b'', entry='https://api.binance.com/api/v3'):
        self.entry = entry
        self.key = key
        self.secret = secret
        
    def _check_keys(self):
        if self.key == '' or self.secret == '':
            return camelq_result(1000, 'Private API is unuseable.Key or Secret is empty.')
        else:
            return camelq_result(0, )

    def get_executions(self, product_code):
        '''Get all record of execution.'''
        response = requests.get(self.entry + '/executions?product_code=' + product_code)
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))

    def get_ticker(self, product_code):
        '''Get ticker.'''
        response = requests.get(self.entry + '/ticker/price?symbol=' + product_code)
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))

    def get_boardstate(self, product_code):
        '''Get the state of product.'''
        response = requests.get(self.entry + '/getboardstate?product_code=' + product_code)
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))

    def get_balance(self):
        '''Get balance.'''
        res = self._check_keys()
        if res['result_code'] != 0:
            return res
        now_timestamp = str(int(datetime.datetime.now(datetime.timezone.utc).timestamp))
        method = 'POST'
        path = '/me/getbalance'
        message = now_timestamp + method + path
        sign = hmac.new(self.secret, message.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
            'ACCESS-KEY': self.key,
            'ACCESS-TIMESTAMP': now_timestamp,
            'ACCESS-SIGN': sign,
            'Content-Type': 'application/json'
        }
        response = requests.post(self.entry + path, headers=headers)
        if response.status_code == 200:
            return camelq_result(0, response.text)
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))
