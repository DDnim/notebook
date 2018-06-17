import postgresql

def get_db_connection():
    return postgresql.open("pq://sundongyang:postgres@127.0.0.1/postgres")