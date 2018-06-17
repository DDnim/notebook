from stock.currency import item as currency
from stock.product import item as product

class stock_list():
    def __init__(self):
        self._list = dict()

    def __setitem__(self, index, value):
        self._list[index] = value

    def __getitem__(self, index, objtype=None):
        if index in self._list:
            return self._list[index]
        else:
            self._list[index] = product()
            return self._list[index]

class account():
    def __init__(self, currency_name = 'jpy'):
        self.stock_list = stock_list()
        self._currency_name = currency_name
        self.stock_list[currency_name] = currency('jpy','jpy')
        self.profit = 0
        self.value = 0
    
    @property
    def balance(self):
        return None

    @balance.setter
    def balance(self, v):
        self.stock_list[self._currency_name].price = v

    @balance.getter
    def balance(self):
        return self.stock_list[self._currency_name].price


    def refresh(self):
        return 0