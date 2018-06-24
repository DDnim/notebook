import logging
import threading

from database import bitflyer as database
from market_api import bitflyer as market_api


class work_bitflyer(object):
    def __init__(self, stock_name):
        self.lock = threading.Lock()
        self._init_sql(stock_name)

        self.stock_name = stock_name
        self.min_partition_size = 10000
        self.max_id = market_api.get_execution_max_id(stock_name)
        self.min_id = 0
        fr = self.sql_get_min_id()[0][0]
        if fr is not None:
            self.min_id = fr
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self._work_list = {}

        self._insert_job_list(0)
        self._create_job_list()
        
        self.value = 1

    def get_serial(self):
        self.lock.acquire()
        try:
            for x in self._work_list.keys():
                if self._work_list[x]['working'] == '0' and self._work_list[x]['worked'] == '0':
                    self._work_list[x]['working'] = '1'
                    return [self._work_list[x]['id_fr'],self._work_list[x]['id_to']]
        finally:
            self.lock.release()

    def set_complite(self, id_fr):
        self.lock.acquire()
        try:
            self.logger.info('>>'+'{:.3%}'.format(((id_fr - self.min_id)/(self.max_id - self.min_id))) + '<< ' + self.stock_name + '>>'+'{:.3%}'.format(((id_fr)/(self.max_id))) + '<< ')
            self.sql_complite_partition(id_fr)
            self._work_list[id_fr]['worked'] = '1'
            self._work_list[id_fr]['working'] = '0'
        finally:
            self.lock.release()

    def _init_sql(self, stock_name):
        DataBaseConnection = database.get_db_cur()
        self.sql_get_min_id = DataBaseConnection.execute("SELECT MAX(id) FROM BITFLYER_EXECUTIONS_" + stock_name)
        self.sql_create_new_partition = DataBaseConnection.execute("INSERT INTO bitflyer_executions_" + stock_name + "_partition SELECT $1,$2,$3 WHERE NOT EXISTS (SELECT id_fr FROM bitflyer_executions_" + stock_name + "_partition WHERE id_fr = $1)")
        self.sql_get_unworked_partition = DataBaseConnection.execute("SELECT *,'0' FROM bitflyer_executions_" + stock_name + "_partition WHERE complited = '0' ORDER BY id_fr")
        self.sql_complite_partition = DataBaseConnection.execute("UPDATE bitflyer_executions_" + stock_name + "_partition SET complited = '1' WHERE id_fr = $1")

    def _insert_job_list(self, min_id):
        for i in range(min_id, self.max_id, self.min_partition_size):
            if i + self.min_partition_size - 1 < self.max_id:
                self.sql_create_new_partition(i, i + self.min_partition_size - 1,'0')

    def _create_job_list(self):
        data = self.sql_get_unworked_partition()
        for row in data:
            self._work_list.update({row[0]:{'id_fr':row[0],'id_to':row[1],'worked':row[2],'working':row[3]}})
