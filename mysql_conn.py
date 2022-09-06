# haimtran 05 SEP 2022
# rds mysql iops
import datetime
import json
import uuid
import logging as logger
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import mysql.connector

# 
logger.basicConfig(level=logger.DEBUG)

# parameter
NUM_ROW = 10000
CHUNK_SIZE = 100
NUM_THREAD_WORKER = 100


with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


def get_connect():
    conn = mysql.connector.connect(
        host=config["ENDPOINT"],
        user=config["USER"],
        password=config["PASS"],
        database=config["DB"],
    )
    return conn


def create_table() -> None:
    """
    create a rds table
    """
    # get connection 
    conn = get_connect()
    # cursor
    cur = conn.cursor()
    # drop table if exists
    drop = "DROP TABLE IF EXISTS employees"
    cur.execute(drop)
    # create table
    employee_table = (
        "CREATE TABLE employees ("
        "    id VARCHAR(36) UNIQUE, "
        "    name VARCHAR(200) DEFAULT '' NOT NULL, "
        "    age INT, "
        "    time TEXT, "
        "PRIMARY KEY (id))"
    )
    cur.execute(employee_table)
    cur.close()
    conn.close()


def fetch_data():
    """
    fetch data
    """
    # get connection 
    conn = get_connect()
    # output
    items = []
    # cursor connector
    cur = conn.cursor()
    #
    stmt_select = (
        "SELECT * FROM mytesttable"
    )
    cur.execute(stmt_select)
    # parse
    for row in cur.fetchall():
        items.append(row)
        print(row)
    # close connection 
    cur.close()
    conn.close()
    # return
    return items


def write_to_table():
    # get connection
    conn = get_connect()
    conn.autocommit = True
    print(f"thread {current_thread().name} connect {conn}")
    cursor = conn.cursor()
    print(f"thread {current_thread().name} cursor {cursor}")
    for k in range(NUM_ROW):
        print(f"{current_thread().name} insert item {k}")
        stmt_insert = "INSERT INTO employees (id, name, age, time) VALUES (%s, %s, %s, %s)"
        cursor.execute(stmt_insert, (str(uuid.uuid4()), f"{str(uuid.uuid4())}-{str(uuid.uuid4())}", 30, datetime.datetime.now().strftime('%Y-%M-%D-%H-%M-%S')))
        if k % CHUNK_SIZE == 0: 
            print(f"{current_thread().name} commit chunk {k // CHUNK_SIZE}")
            conn.commit()
    # close connection
    cursor.close()
    conn.close()


def run_mysql(workload):
    """thread worker function"""
    # Connect to the database
    db = get_connect()
    # 
    print(f"{current_thread().name} connect {db}")
    db.autocommit = True
    cursor = db.cursor()
    if workload == 'insert':
        sql = "INSERT INTO myschema.mytesttable (id_pk,random_string,random_number,reverse_string,row_ts) " \
              "VALUES(replace(uuid(),'-',''),concat(replace(uuid(),'-',''), replace(convert(rand(), char), '.', ''), " \
              "replace(convert(rand(), char), '.', '')),rand(),reverse(concat(replace(uuid(),'-',''), " \
              "replace(convert(rand(), char), '.', ''), replace(convert(rand(), char), '.', ''))),current_timestamp)"
        logger.debug('statement being issued %s', sql)
    else:
        workload = 'query'
        sql = "SELECT COUNT(*) as result_value FROM myschema.mytesttable"
        logger.debug('executing %s', sql)

    for i in range (NUM_ROW):
        cursor.execute(sql)
        if workload == 'query':
            row = cursor.fetchall()
            logger.debug(f"fetched rows {row}")
        # commit the rows periodically
        # write out a message indicating that progress is being made
        if i % CHUNK_SIZE == 0:
            logger.debug(f"{current_thread().name} commit {i}")
            db.commit()
    # commit the outstanding rows
    db.commit()
    db.close()
    return


def thread_load_write_test():
    with ThreadPoolExecutor(max_workers=NUM_THREAD_WORKER) as executor:
        for k in range(1, NUM_THREAD_WORKER+1):
            print(f"submit {k} thread")
            executor.submit(run_mysql, "insert")



if __name__ == "__main__":
   # create_table()
   thread_load_write_test()
   # fetch_data()
