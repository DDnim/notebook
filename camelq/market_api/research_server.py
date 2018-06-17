import research_server.research_server as rs
import pandas
import time

class research():
    def __init__(self, p_account = None):
        self._connection = rs.server(p_account)

    def get_balance(self):
        self._connection.requests({'command' : 'get_balance'})

    def order(self, side, product, size, price):
        self._connection.requests({'command' : 'order'
                                    , 'side' : side
                                    , 'product' : product
                                    , 'size' : size
                                    , 'price' : price
                                    })