import requests
import datetime
import hashlib, hmac, json
from common import *

class bitflyer():
    def __init__(self, key='', secret='', entry='https://api.bitflyer.jp'):
        self.entry = entry
        self.key = key
        self.secret = secret.encode('utf-8')
        
    def _check_keys(self):
        if self.key == '' or self.secret == '':
            return camelq_result(1000, 'Private API is unuseable.Key or Secret was unset.')
        else:
            return camelq_result(0, )

    def get_executions(self, product_code):
        '''Get all record of execution.'''
        response = requests.get(self.entry + '/v1/executions?product_code=' + product_code)
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))

    def get_ticker(self, product_code):
        '''Get ticker.'''
        response = requests.get(self.entry + '/v1/getticker?product_code=' + product_code)
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))

    def get_boardstate(self, product_code):
        '''Get the state of product.'''
        response = requests.get(self.entry + '/v1/getboardstate?product_code=' + product_code)
        if response.status_code == 200:
            return camelq_result(0, json.loads(response.text))
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code))

    def get_balance(self):
        '''Get balance.'''
        res = self._check_keys()
        if res['result_code'] != 0:
            return res
        now_timestamp = str(int(datetime.datetime.now(datetime.timezone.utc).timestamp()))
        body = json.dumps({ })
        method = 'GET'
        path = '/v1/me/getbalance'
        message = now_timestamp + method + path + body
        sign = hmac.new(self.secret, message.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
            'ACCESS-KEY': self.key,
            'ACCESS-TIMESTAMP': now_timestamp,
            'ACCESS-SIGN': sign,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(self.entry + path, data=body, headers=headers)
        if response.status_code == 200:
            return camelq_result(0, response.text)
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code) + response.text)


    def get_positions(self, market):
        now = datetime.datetime.now(datetime.timezone.utc)
        now_timestamp = str(int(now.timestamp()))

        method = 'GET'
        path = '/v1/me/getpositions?product_code=' + market
        body = json.dumps({'product_code': market})
        message = now_timestamp + method + path + body
        sign = hmac.new(self.secret, message.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
            'ACCESS-KEY': self.key,
            'ACCESS-TIMESTAMP': now_timestamp,
            'ACCESS-SIGN': sign,
            'Content-Type': 'application/json'
        }
        response = requests.get(self.entry + path, data=body, headers=headers)
        if response.status_code == 200:
            return camelq_result(0, response.text)
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code) + response.text)


    def request_order(self, market, side, price, size, order_type='MARKET'):
        now = datetime.datetime.now(datetime.timezone.utc)
        now_timestamp = str(int(now.timestamp()))
        method = 'POST'
        path = '/v1/me/sendchildorder'
        body = json.dumps({
        'product_code': market,
        'child_order_type': order_type,
        'side': side,
        'price': price,
        'size': size
        })
        message = now_timestamp + method + path + body
        sign = hmac.new(self.secret, message.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
            'ACCESS-KEY': self.key,
            'ACCESS-TIMESTAMP': now_timestamp,
            'ACCESS-SIGN': sign,
            'Content-Type': 'application/json'
        }
        response = requests.post(self.entry + path, data=body, headers=headers)
        if response.status_code == 200:
            return camelq_result(0, response.text)
        else:
            return camelq_result(100, 'Request error: ' + str(response.status_code) + response.text)
