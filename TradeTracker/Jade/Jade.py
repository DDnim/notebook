import threading
import time
from Market import BitFlyer

def refresh(market, stock_list, thread_count=1):
    work_thread = []
    for stock in stock_list:
        work_thread.append(threading.Thread(target=eval(market).get_data, args=(stock, 16,)))
        time.sleep(1)
        work_thread[-1].start()


def refresh_multiple_market(market_list, stock_list):
    work_thread = []
    market_count = len(market_list)
    for i in range(0, market_count - 1):
        work_thread.append(threading.Thread(target=refresh, args=(market_list[i],stock_list[i])))
        work_thread[-1].start()

refresh('BitFlyer',['FX_BTC_JPY'],16)