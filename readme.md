## Introduction
- iops and cost 
- test and monitor iops 
- load data.csv into a table
- intensive io schema [here](https://github.com/aws-samples/specialty-practice-code-samples/blob/master/choose-between-gp2-and-io1/mysql-create-table.sql)

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
mysql -h $ENDPOINT -P 3306 -u $USER -p
```
then run the schmea.sql to create table and index with intensive io pattern 

## Experiment
db.m6l.large 2vCPU 8GB 20GB GP2 

![Screen Shot 2022-09-06 at 12 30 43](https://user-images.githubusercontent.com/20411077/188558643-98258fd0-c685-4945-b415-4caa9bfa7827.png)


db.m6l.large 2vCPU 8GB **provisioned 3000** IOPS and 100GB SSD 

![Screen Shot 2022-09-06 at 13 00 16](https://user-images.githubusercontent.com/20411077/188558305-1d9cbc7a-8816-47bb-a6d3-583a8a08d35b.png)

![Screen Shot 2022-09-06 at 12 59 58](https://user-images.githubusercontent.com/20411077/188558313-be48b64d-c885-493c-b48a-5b58bdcf6712.png)

db.m5.4xlarge 16vCPU 64GB provisioned 3000 IOPS and 400GB SSD 

![Screen Shot 2022-09-06 at 13 03 05](https://user-images.githubusercontent.com/20411077/188558541-fa551243-5840-41d2-99c7-fafa3a2ec8d9.png)

![Screen Shot 2022-09-06 at 13 03 17](https://user-images.githubusercontent.com/20411077/188558550-23342ec9-a082-4219-b562-c6113caadddf.png)


## Troubleshooting 
basic sql show databases 
```sql
show databases; 
```

show tables 
```sql 
show tables; 
```

query a table 
```sql 
select * from employess limit 10; 
```

insert 
```sql 
insert into employees (id, name, age, time) values  ('haimtran001', 'haimtran', 30, '2022-49-09/06/22-03-49-38');
```

drop table 
```sql
drop table employess; 
```


## Reference 
1. [understanding burst mode](https://aws.amazon.com/blogs/database/understanding-burst-vs-baseline-performance-with-amazon-rds-and-gp2/)

2. [metric provisioned iops](https://aws.amazon.com/blogs/database/how-to-use-cloudwatch-metrics-to-decide-between-general-purpose-or-provisioned-iops-for-your-rds-database/)

3. [cpu burstable instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html)

4. [cpu burstable ec2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html)

5. [data](https://aws-blogs-artifacts-public.s3.amazonaws.com/artifacts/DBBLOG-1922/sample-dataset.zip)

