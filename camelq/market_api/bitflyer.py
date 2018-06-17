import requests
import pandas
import time


def get_execution_max_id(stock_name):
    '''Get the last record of execution.'''
    response = requests.get('https://api.bitflyer.jp/v1/executions?product_code=' + stock_name)
    if response.status_code == 200:
        data = pandas.read_json(response.text)
        return data.id[0]
    else:
        time.sleep(5)
        return -1


