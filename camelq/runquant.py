import sys
import json

import quant.TestTrade_MA20180708 as quant


setting = json.load(open(sys.path[0] + '/' + sys.argv[1], 'r'))

q = quant.quant(setting)
q.run()