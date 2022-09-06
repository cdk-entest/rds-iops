'''
haimtran load csv into rds mysql table
'''

import json
import pymysql
import sys

with open("config.json", 'r', encoding='utf-8') as file:
    configs = json.load(file)


def mysql_execute_command(sql, db_host, db_username, db_password):
    '''
    This function excutes the sql statement, does not return any value.
    '''
    try:
        con = pymysql.connect(host=db_host,
                                user=db_username,
                                password=db_password,
                                autocommit=True,
                                local_infile=1)
        # Create cursor and execute SQL statement
        cursor = con.cursor()
        cursor.execute(sql)
        con.close()
       
    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)


def initialize_database(configs):
    '''
    This function initialize the MySQL database if not already done so and generates
    all configurations needed for the application.
    ''' 
   
    # Initialize Database
    print ('Initializing MySQL Database...')

    #Drop table if exists
    sql_command = "DROP TABLE IF EXISTS mydb.articles;"
    mysql_execute_command(sql_command, configs['ENDPOINT'], configs['USER'], configs['PASS'])

    #Create table
    sql_command = "CREATE TABLE mydb.articles (OBJECTID INT, SHA TEXT, PossiblePlace TEXT, Sentence TEXT, MatchedPlace TEXT, DOI  TEXT, Title TEXT, Abstract TEXT, PublishedDate TEXT, Authors TEXT, Journal TEXT, Source TEXT, License TEXT, PRIMARY KEY (OBJECTID));"
    mysql_execute_command(sql_command, configs['ENDPOINT'], configs['USER'], configs['PASS'])

    #Load CSV file into mysql
    sql_command = """
    LOAD DATA LOCAL INFILE '{0}' 
    INTO TABLE mydb.articles 
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;
    """.format(configs['dataset_file'])
    mysql_execute_command(sql_command, configs['ENDPOINT'], configs['USER'], configs['PASS'])


def mysql_fetch_data(sql, db_host, db_username, db_password, db_name):
    '''
    This function excutes the sql query and returns dataset.
    '''
    try:
        con = pymysql.connect(host=db_host,
                                user=db_username,
                                password=db_password,
                                database=db_name,
                                autocommit=True,
                                local_infile=1,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)                              
        # Create cursor and execute SQL statement
        cursor = con.cursor()
        cursor.execute(sql)
        data_set = cursor.fetchall()
        con.close()
        print(data_set)
        return data_set
       
    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)



max_rows = 500
db_table = 'articles'
db_tbl_fields = ['OBJECTID', 'Sentence', 'Title', 'Source']
sql_fields = ', '.join(db_tbl_fields)
sql = "select SQL_NO_CACHE " + sql_fields + " from " + db_table  +  " where  Sentence like '%delta%' order by OBJECTID limit " + str(max_rows)


if __name__=="__main__":
#    initialize_database(configs)
    mysql_fetch_data(sql, configs['ENDPOINT'], configs['USER'], configs['PASS'], configs['DB'])
