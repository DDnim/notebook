import requests
import pandas
import postgresql
from datetime import datetime as dt
import time
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def request_data_refresh(id_fr, id_to, market):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    body = {'product_code': market}

    DataBaseConnection = postgresql.open("pq://sundongyang:postgres@127.0.0.1/postgres")
    executions_max_id_per = DataBaseConnection.prepare("SELECT MAX(id) FROM BITFLYER_EXECUTIONS_BTC_FX_JPY WHERE id between $1 and $2")

    executions_insert = DataBaseConnection.prepare(
        "INSERT INTO BITFLYER_EXECUTIONS_BTC_FX_JPY(id, u_time, price, side, size) SELECT $1, $2, $3, $4, $5 WHERE NOT EXISTS (SELECT id FROM BITFLYER_EXECUTIONS_BTC_FX_JPY WHERE id = $6) ")

    fr = executions_max_id_per(id_fr, id_to)[0][0] + 1
    if fr is not None:
        id_fr = fr

    # 开始取得数据
    logger.debug(str(id_fr)+ '->' + str(id_to))

    for z in range(id_fr, id_to, 100):
        try:
            response = requests.get('https://api.bitflyer.jp/v1/executions?product_code=' + market
                                    + '&before=' + str(z + 100)
                                    + '&after=' + str(z), data=body)
            if response.status_code < 300:
                data = pandas.read_json(response.text, convert_dates='exec_date',)

                for i in range(0,len(data)):
                    if len(data.exec_date[i]) > 19:
                        t = time.mktime(
                            dt.strptime(data.exec_date[i].replace('T', ' '), '%Y-%m-%d %H:%M:%S.%f').timetuple())
                    else:
                        t = time.mktime(
                            dt.strptime(data.exec_date[i].replace('T', ' '), '%Y-%m-%d %H:%M:%S').timetuple())
                    executions_insert(data['id'][i], t, float(data['price'][i]), data['side'][i][:1], data['size'][i],data['id'][i])
                logger.info('>>'+'{:.3%}'.format(((z - id_fr) / (id_to - id_fr))) + '<< ' + market)
            else:
                logger.debug(response.status_code)
                z = z - 100
                time.sleep(10)
        except Exception as e:
            logger.debug(e)


def get_data(market, threads):
    fr = 0
    to = 200000000

    work_load = (to - fr) / threads

    work_thread = []
    for i in range(1, threads + 1):
        time.sleep(1)
        logging.debug(str(market) + str(int(fr + (i - 1) * work_load)) + str(int(fr + i * work_load - 1)))
        work_thread.append(threading.Thread(target=request_data_refresh,
                                          args=(int(fr + (i - 1) * work_load), int(fr + i * work_load - 1), market,)))
        work_thread[i-1].start()

def test():
    logging.debug(1)