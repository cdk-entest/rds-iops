import sys
import time
import mysql.connector as my
import boto3
import botocore
import simplejson as json
import threading
import logging

# connect to mysql using the token or password and insert 100k rows of data
def run_mysql(workload):
    """thread worker function"""
    # Connect to the database
    db = my.connect(host=connvals['host'],
                    user=connvals['user'],
                    password=mytoken,
                    db=connvals['db'],
                    ssl_ca=connvals['ssl']
                    )
    db.autocommit = True
    logger.debug('connecting to %s as %s', connvals['host'], connvals['user'])
    cursor = db.cursor()
    
    if workload == 'insert':
        sql = "INSERT INTO myschema.mytesttable (id_pk,random_string,random_number,reverse_string,row_ts) " \
              "VALUES(replace(uuid(),'-',''),concat(replace(uuid(),'-',''), replace(convert(rand(), char), '.', ''), " \
              "replace(convert(rand(), char), '.', '')),rand(),reverse(concat(replace(uuid(),'-',''), " \
              "replace(convert(rand(), char), '.', ''), replace(convert(rand(), char), '.', ''))),current_timestamp)"
        logger.debug('statement being issued %s', sql)
    else:
        workload = 'query'
        sql = "SELECT COUNT(*) as result_value FROM myschema.mytesttable WHERE random_number > rand() LIMIT 100"
        logger.debug('executing %s', sql)

    for i in range (100000):
        cursor.execute(sql)
        if workload == 'query':
            row = cursor.fetchall()
            logger.debug("fetched rows")
        # commit the rows periodically
        # write out a message indicating that progress is being made
        if i % 10000 == 0:
            logger.debug("completed %s executions and commit", str(i))
            db.commit()
    # commit the outstanding rows
    db.commit()
    db.close()
    return

# main program
def main():
    logger.debug('inside main')
    workload=sys.argv[1]
    run_mysql(workload)

if __name__== "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler('output.log')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    # start the logging session
    logger.debug('Start of log...')

    numthreads=int(sys.argv[2])
    # insert or query some data in mysql
    for i in range(numthreads):
        t = threading.Thread(target=main)
        t.setDaemon(True)
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join()
