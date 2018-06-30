from account.account import account
from stock.product import item
import stock

x = account()

x.stock_list.update({'12' : item('123','345')})
x.stock_list.update({'13' : item('124','345')})

o_l = dict()
for s in x.stock_list.items():
    o = s[1]
    if type(o) != type(stock.currency.item()):
        o_l.update({s[0] : {'name' : o.name, 'code' : o.code, 'price' : o.price, 'size' : o.size}})

if '12' in x.stock_list.keys():
    print(o_l)