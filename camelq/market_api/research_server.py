import research_server.research_server as rs
import pandas
import time

class research():
    def __init__(self, p_account = None):
        self._connection = rs.server(p_account)

    def get_balance(self):
        return self._connection.get({'command' : 'get_balance'})
        

    def get_executions(self):
        return self._connection.get({'command' : 'get_executions'})

    def order(self, side, product, size, price, time=0):
        self._connection.post({'command' : 'order'
                                    , 'side' : side
                                    , 'product' : product
                                    , 'size' : size
                                    , 'price' : price
                                    , 'time' : time
                                    })
    
    def get_tick(self, name, time):
        return self._connection.get({'command' : 'get_tick' ,'time' : time})

    def set_lantecy(self, t):
        self._connection.lantecy = t