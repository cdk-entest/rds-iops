## Introduction
- iops and cost 
- test and monitor iops 
- load data.csv into a table

## Connect 
install mysql client and connect 
```bash 
sudo yum install mariadb
```
and check 
```bash 
mysql --version
```
then connect with endpoint, and username and then provide password when asked 
```bash 
mysql -h mysql–instance1.123456789012.us-east-1.rds.amazonaws.com -P 3306 -u mymasteruser -p
```
basic sql 
show databases 
```sql 
show databases; 
```
show tables 
```sql
use mydb; 
show tables; 
```
query a table 
```sql
select * from employess limit 10; 
```
insert 
```sqs
insert into employees (id, name, age, time) values  ('haimtran001', 'haimtran', 30, '2022-49-09/06/22-03-49-38');
```
query 
```sql
select * from employees where id='haimtran001'; 
```
drop table 
```sql
drop table employees; 
```

## Intensive IO Schema 
```
-- create a schema if it doesn't already exist
CREATE SCHEMA IF NOT EXISTS myschema;
-- drop the table if it is already there (dropping the table first will provide for a clean run)
DROP TABLE myschema.mytesttable;
-- create a simple table
CREATE TABLE IF NOT EXISTS  myschema.mytesttable (
  id_pk             varchar(36)     not null,
  random_string     varchar(200)    not null,
  random_number     double          not null,
  reverse_string    varchar(200)    not null,
  row_ts            timestamp       not null,
 PRIMARY KEY (id_pk)
);
-- create a few indexes to better support a real I/O scenario
CREATE INDEX rs_secondary_idx ON myschema.mytesttable (random_string);
CREATE INDEX rn_secondary_idx ON myschema.mytesttable (random_number);
CREATE INDEX ts_secondary_idx ON myschema.mytesttable (row_ts);
CREATE INDEX ci_compound_idx ON myschema.mytesttable (reverse_string, id_pk);

-- Replace existing <mydbuser> with your own database user
GRANT SELECT, INSERT, UPDATE, DELETE on myschema.mytesttable TO <mydbuser>;

-- sample SQL for generating some random data
INSERT INTO myschema.mytesttable
(id_pk,
 random_string,
 random_number,
 reverse_string,
 row_ts
)
VALUES
(replace(uuid(),'-',''),
 concat(replace(uuid(),'-',''), replace(convert(rand(), char), '.', ''), replace(convert(rand(), char), '.', '')),
 rand(),
 reverse(concat(replace(uuid(),'-',''), replace(convert(rand(), char), '.', ''), replace(convert(rand(), char), '.', ''))),
 current_timestamp
);

```

## Experiment
db.m6l.large 2vCPU 8GB 20GB GP2 


db.m6l.large 2vCPU 8GB provisioned 3000 IOPS and 100GB SSD 


db.m5.4xlarge 16vCPU 64GB provisioned 3000 IOPS and 400GB SSD 


## Reference 
1. [understanding burst mode](https://aws.amazon.com/blogs/database/understanding-burst-vs-baseline-performance-with-amazon-rds-and-gp2/)

2. [metric provisioned iops](https://aws.amazon.com/blogs/database/how-to-use-cloudwatch-metrics-to-decide-between-general-purpose-or-provisioned-iops-for-your-rds-database/)

3. [cpu burstable instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html)

4. [cpu burstable ec2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html)

5. [data](https://aws-blogs-artifacts-public.s3.amazonaws.com/artifacts/DBBLOG-1922/sample-dataset.zip)

