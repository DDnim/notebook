import datetime,time

base_data = "2018-01-02"
date_time = time.strptime(base_data, "%Y-%M-%d")
unix_time = int(time.mktime(date_time))
print(unix_time)

for i in range(unix_time, int(time.mktime(datetime.datetime.now().timetuple())), 86400):
    print(i)