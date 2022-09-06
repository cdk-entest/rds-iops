# haimtran 05 SEP 2022
# rds mysql iops
import datetime
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import mysql.connector

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



def thread_load_write_test():
    with ThreadPoolExecutor(max_workers=NUM_THREAD_WORKER) as executor:
        for k in range(1, NUM_THREAD_WORKER+1):
            print(f"submit {k} thread")
            executor.submit(write_to_table)

if __name__ == "__main__":
    create_table()
    thread_load_write_test()
    #fetch_data()
