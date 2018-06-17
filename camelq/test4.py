
from account.account import account
from market_api.research_server import research

a = account()
a.balance = 12345

server = research(a)
server.get_balance()
server.order()
