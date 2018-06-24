import psycopg2

def get_db_cur():
    cn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=postgres user=sundongyang password=postgres")
    return cn.cursor()
