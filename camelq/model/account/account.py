from model.stock.currency import item as currency
from model.stock.product import item as product

class account():
    def __init__(self, currency_name = 'jpy'):
        self.stock_list = dict()
        self._currency_name = currency_name
        self.stock_list.update({currency_name : currency('jpy','jpy')})
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

    def add_stock(self, name, code = ''):
        self.stock_list.update({name : currency(name, code)})
        
        