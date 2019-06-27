import pymysql

def connection():
    conn = pymysql.connect(host='localhost',
                             db='capstone',
                             user='root',
                             passwd='India@09')
    cur = conn.cursor()

    return cur,conn