# haimtran 05 SEP 2022 
# connect to rds mycrosoft sql 
# enable fish shell first

import json
import pymssql

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

# connection
conn = pymssql.connect(
    server= config['ENDPOINT'],
    port= config['PORT'],
    user=config['USER'],
    password=config['PASS'],
    database='tempdb'
)

def create_table():
    # cursor
    cur = conn.cursor()
    # create table
    employee_table = (
        """
        IF OBJECT_ID('persons', 'U') IS NOT NULL
        DROP TABLE persons
        CREATE TABLE persons (
        id INT NOT NULL,
        name VARCHAR(100),
        salesrep VARCHAR(100),
        PRIMARY KEY(id)
        )
        """
    )
    cur.execute(employee_table)
    # insert some data 
    cur.executemany(
    "INSERT INTO persons VALUES (%d, %s, %s)",
    [(1, 'John Smith', 'John Doe'),
     (2, 'Jane Doe', 'Joe Dog'),
     (3, 'Mike T.', 'Sarah H.')])
    # 
    conn.commit()

def query_table():
    # cursor
    cursor = conn.cursor()
    # list table
    cursor.execute('SELECT * FROM persons')
    row = cursor.fetchone()
    while row:
        print("ID=%d, Name=%s" % (row[0], row[1]))
        row = cursor.fetchone()



if __name__=="__main__":
    # create_table()
    query_table()
