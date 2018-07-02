import multiprocessing
import time
import logging
import database.bitflyer as db
from model.account.account import account
import model.stock as stock

logging.basicConfig(level=logging.ERROR)

class server():
    def __init__(self, p_account=None):
        self._q = multiprocessing.Queue()
        self._e = multiprocessing.Event()
        self._re = multiprocessing.Event()
        self._rq = multiprocessing.Queue()
        self.lantecy = 0
        self.commission = 0.0015
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
            logging.debug('Got Event')
            self._e.clear()
            while not q.empty():
                self._event_manager(self._q.get())


    def post(self, p):
        self._q.put(p, True)
        self._e.set()

    def get(self, p):
        self._q.put(p, True)
        # self._q.close()
        # self._q.join_thread()
        # time.sleep(0.1)
        self._e.set()
        while not self._re.wait(0.01):
            self._e.set()
        self._re.clear()
        return self._rq.get()

    def _event_manager(self, p):
        logging.info(p)
        if type(p['command']) != str:
            logging.error('Parameter 1 have to be str.Given ' + str(type(p[0])))
        if p['command'].lower() == 'order':
            self._order(p)
        elif p['command'].lower() == 'cancel':
            pass
        elif p['command'].lower() == 'get_balance':
            self._rq.put(self.account.balance)
            self._re.set()
        elif p['command'].lower() == 'get_executions':
            self._rq.put(self._get_executions())
            self._re.set()
        elif p['command'].lower() == 'get_tick':
            self._rq.put(self._get_tick(p))
            self._re.set()

    def _order(self, p):
        if p['time'] == 0:
            price = self.account.stock_list[p['product']].price
        else:
            price = float(self._get_tick(p)['price'])
        if p['side'] == 'buy':
            if self.account.balance > round(price * int(p['size']) + price * int(p['size']) * self.commission):
                if p['product'] in self.account.stock_list.keys():
                    self.account.stock_list[p['product']].size = self.account.stock_list[p['product']].size + int(p['size'])
                    self.account.balance = self.account.balance - round(price * int(p['size']) * (1 - self.commission))
                else:
                    self.account.add_stock(p['product'],'123')
                    self.account.stock_list[p['product']].size = 0 + int(p['size'])
                    self.account.balance = self.account.balance - round(price * int(p['size']) * (1 - self.commission))
            else:
                logging.error('Balance is not enough')
        elif p['side'] == 'sell':
            if self.account.stock_list[p['product']].size >= int(p['size']):
                self.account.stock_list[p['product']].size = self.account.stock_list[p['product']].size - int(p['size'])
                self.account.balance = self.account.balance +  round( price * int(p['size']) * (1 - self.commission))
            else:
                logging.error('Product is not enough')
        #logging.info({'order_size' : int(p['size']), 'product_size' : self.account.stock_list[p['product']].size, 'currency_balance' : self.account.balance, 'product_price' : price})

    def _get_tick(self, p):
        cur = db.get_db_cur()
        query_sql = "SELECT * FROM bitflyer_executions_btc_jpy where id = (SELECT min(id) FROM bitflyer_executions_btc_jpy WHERE u_time = (SELECT MIN(u_time) FROM bitflyer_executions_btc_jpy where u_time > {}))".format(p['time'] + self.lantecy)
        logging.debug(query_sql)
        cur.execute(query_sql)

        column_names = [desc[0] for desc in cur.description]

        d = dict()
        for row in cur:
            d.update(zip(column_names,row))

        return d

    def _get_executions(self):
        o_l = dict()
        for s in self.account.stock_list.items():
            o = s[1]
            if type(o) != type(stock.currency.item()):
                o_l.update({s[0] : {'name' : o.name, 'code' : o.code, 'price' : o.price, 'size' : o.size}})
        return o_l
