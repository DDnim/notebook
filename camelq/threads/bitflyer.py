import logging
import threading
import time
from datetime import datetime as dt

import pandas
import postgresql
import requests

from works.bitflyer import work_bitflyer as works

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


def request_data_refresh(market, works_object):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('Start')
    
    while True:
        id_fr, id_to = works_object.get_serial()
        logger.debug([id_fr,id_to])

        body = {'product_code': market}

        DataBaseConnection = postgresql.open("pq://sundongyang:postgres@127.0.0.1/postgres")
        executions_insert = DataBaseConnection.prepare(
            "INSERT INTO BITFLYER_EXECUTIONS_" + market + "(id, u_time, price, side, size) SELECT $1, $2, $3, $4, $5 WHERE NOT EXISTS (SELECT id FROM BITFLYER_EXECUTIONS_" + market + " WHERE id = $6) ")

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
                    logger.debug('>>'+'{:.3%}'.format(((z - id_fr) / (id_to - id_fr))) + '<< ' + market)
                else:
                    logger.debug(response.status_code)
                    z = z - 100
                    time.sleep(10)
            except Exception as e:
                logger.debug(e)
        works_object.set_complite(id_fr)


def get_data(market, threads):
    work = works(market)
    work_thread = []
    for i in range(1, threads + 1):
        time.sleep(1)
        work_thread.append(threading.Thread(target=request_data_refresh,
                                          args=(market, work,)))
        work_thread[i-1].start()
