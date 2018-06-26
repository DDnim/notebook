from database import bitflyer as database
import pandas
import datetime,time
import numpy
class indicator_bitflyer():
    def __init__(self, stock_name):
        self._init_sql()
        self.stock_name = stock_name
    
    def _refresh_ohlc(self, time_from, time_to):
        fr = int(time.mktime(time.strptime(time_from, "%Y-%m-%d %H:%M:%S")))
        to = int(time.mktime(time.strptime(time_to, "%Y-%m-%d %H:%M:%S")))
        db_fr = int(time.mktime(time.strptime(self.select_ohlc_max()[0][0], "%Y-%m-%d %H:%M:%S")))

        if db_fr > to:
            return

        if db_fr > fr:
            fr = db_fr
        
        for i in range(fr, to, 86400):
            data = self.sql_get_all(i, i + 86400 - 1)
            df = pandas.DataFrame(data, columns=['u_time','price'],dtype='float')
            df['Time'] = pandas.to_datetime(df.u_time, unit='s')
            dateTimeIndex = pandas.DatetimeIndex(df['Time'])
            df.index = dateTimeIndex
            ohlc = df.price.resample('T', how='ohlc')
            for index, row in ohlc.dropna().iterrows():
                print(index, row['open'], row['high'], row['low'], row['close'])
                self.insert_ohlc(index, row['open'], row['high'], row['low'], row['close'])
    
    def get_ohlc(self, time_from, time_to = "1980-01-01 00:00:00"):
        # self._refresh_ohlc(time_from, time_to)
        cursor = database.get_db_cur()
        if time_to == "1980-01-01 00:00:00":
            time_to = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("SELECT * FROM bitflyer_executions_{}_ohlc WHERE '{}' <= time and time < '{}'".format(self.stock_name, time_from, time_to))
        column_names = [desc[0] for desc in cursor.description]

        d = dict()
        for row in cursor:
            d.update({row[0].timestamp() : dict(zip(column_names,row))})
        return d
        


    def _init_sql(self):
        pass
        # self.sql_get_all = DataBaseConnection.prepare("SELECT u_time, price FROM bitflyer_executions_" + self.stock_name + " WHERE  $1 <= u_time AND u_time < $2")
        # self.insert_ohlc = DataBaseConnection.prepare("INSERT INTO bitflyer_executions_" + self.stock_name + "_ohlc SELECT $1,$2,$3,$4,$5 WHERE NOT EXISTS (SELECT time FROM bitflyer_executions_" + self.stock_name + "_ohlc WHERE time = $1)")
        # self.select_ohlc = DataBaseConnection.prepare("SELECT * FROM bitflyer_executions_" + self.stock_name + "_ohlc WHERE $1 <= time and time < $2)")
        # self.select_ohlc_max = DataBaseConnection.prepare("SELECT MAX(time) FROM bitflyer_executions_" + self.stock_name + "_ohlc")

