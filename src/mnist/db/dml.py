import pymysql.cursors

def get_conn():
    con = pymysql.connect(host='172.18.0.1',
                             user='mnist',
                             password='1234',
                             database='mnistdb',
                             port=53306,
                             cursorclass=pymysql.cursors.DictCursor)
    return con

def select(query: str, size = -1):
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            try:
                result = cursor.fetchmany(size)
                return result
            except pymysql.err.InternalError as e:
                code, msg = e.args
                result =[code, msg]
                return result

#def dml(sql, file_name, file_full_path, formatted_time, request_user):    
def dml(sql, file_name, file_full_path, formatted_time, request_user):
    connection = get_conn()
    with connection.cursor() as cursor:
        # Create a new record
        cursor.execute(sql, (file_name, file_full_path, formatted_time, request_user))
        # connection is not autocommit by default. So you must commit to save
        # your changes
        connection.commit()
        return cursor.rowcount

def insert(query:str):
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query, parameter)
            conn.commit()
    return result

def update(query:str, *p):
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query, p)
            conn.commit()
    return True
