# haimtran 05 SEP 2022
# rds mysql iops

import datetime
import random
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread, main_thread
import mysql.connector
import names

# parameter
NUM_ROW = 1000
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
        "    id INT UNSIGNED NOT NULL AUTO_INCREMENT, "
        "    name VARCHAR(30) DEFAULT '' NOT NULL, "
        "    age TEXT, "
        "    time TEXT, "
        "PRIMARY KEY (id))"
    )
    cur.execute(employee_table)
    # show table
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    for table in tables:
        print(f"table: {table}")
    # close connect
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
        "SELECT id, name, age, time FROM employees ORDER BY id"
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


def drop_table() -> None:
    """
    drop table
    """
    # get connection 
    conn = get_connect()
    # cursor
    cur = conn.cursor()
    # drop table if exists
    drop = "DROP TABLE IF EXISTS employees"
    # execute
    cur.execute(drop)
    # close connection 
    cur.close()
    conn.close()
    print("DELETED TABLE")


def write_to_table(start_idx = 1):
    # get connection
    conn = get_connect()
    conn.autocommit = True
    print(f"thread {current_thread().name} connect {conn}")
    cursor = conn.cursor()
    print(f"thread {current_thread().name} cursor {cursor}")
    # time stamp
    now = datetime.datetime.now()
    time_stamp = now.strftime("%Y/%m/%d-%H:%M:%S.%f")
    # employees (id, name, age, time)
    name = names.get_full_name()
    print('prepare data ...')
    employees = [
        (
            k,
            name,
            random.randint(20, 100),
            time_stamp,
        )
        for k in range(start_idx, NUM_ROW+start_idx)
    ]
    print('data ready ...')
    # tuple
    print('start inserting ...')
    for k in range(NUM_ROW):
        print(f"{current_thread().name} insert item {k}")
        stmt_insert = "INSERT INTO employees (id, name, age, time) VALUES (%s, %s, %s, %s)"
        cursor.execute(stmt_insert, employees[k])
        if k % CHUNK_SIZE == 0: 
            print(f"{current_thread().name} commit chunk {k // CHUNK_SIZE}")
            conn.commit()
    # close connection
    cursor.close()
    conn.close()

def thread_load_write_test():
    with ThreadPoolExecutor(max_workers=NUM_THREAD_WORKER) as executor:
        for k in range(1, NUM_THREAD_WORKER+1):
            print(f"submit {k} thread")
            executor.submit(write_to_table, k*NUM_ROW+1)

if __name__ == "__main__":
    create_table()
    thread_load_write_test()
    # fetch_data()
