import multiprocessing
import time
import logging
from account.account import account

class server():
    def __init__(self, p_account=None):
        self._q = multiprocessing.Queue()
        self._e = multiprocessing.Event()
        if p_account is None:
            self.account = account()
        else:
            self.account = p_account
        w1 = multiprocessing.Process(name='block', 
                                    target=self.wait_for_event,
                                    args=(self._e,self._q,))
        w1.start()

    def wait_for_event(self, e, q):
        while True:
            self._e.wait()
            logging.info('Got Event')
            self._e.clear()
            while not q.empty():
                self._event_manager(self._q.get())

    def _event_manager(self, p):
        if type(p['command']) != str:
            logging.error('Parameter 1 have to be str.Given ' + str(type(p[0])))
        if p['command'].lower() == 'order':
            print('order')
            self._order(p)
        elif p['command'].lower() == 'cancel':
            print('cancel', p[1], p[2], p[3])
        elif p['command'].lower() == 'get_balance':
            print(self.account.balance)

    def _order(self, p):
        print(int(p['size']), self.account.stock_list[p['product']].size, self.account.balance)
        if p['side'] == 'buy':
            if self.account.balance > self.account.stock_list[p['product']].price * int(p['size']):
                self.account.stock_list[p['product']].size = self.account.stock_list[p['product']].size + int(p['size'])
                self.account.balance = self.account.balance - self.account.stock_list[p['product']].price * int(p['size'])
            else:
                print('Balance is not enough')
        elif p['side'] == 'sell':
            if self.account.stock_list[p['product']].size > int(p['size']):
                self.account.stock_list[p['product']].size = self.account.stock_list[p['product']].size - int(p['size'])
                self.account.balance = self.account.balance + self.account.stock_list[p['product']].price * int(p['size'])
            else:
                print('Product is not enough')
        print(int(p['size']), self.account.stock_list[p['product']].size, self.account.balance)


    def requests(self, p):
        self._q.put(p)
        self._e.set()
