**Healthcare Data Lake \& ETL Pipeline on AWS**



This project demonstrates how to build a **Healthcare Data Lake and ETL Pipeline** using AWS services.  



The pipeline ingests raw patient recovery data, processes it with AWS Glue (PySpark), and makes it available for analytics in Redshift and visualization in QuickSight.



---



**Project Flow**



1\.   Data Source (CSV)

&nbsp;  - Patient demographics, surgery info, recovery time.  



2\.   Amazon S3 (Raw Zone)  

&nbsp;  - Upload raw patient data.  



3\.   AWS Glue Crawler \& Data Catalog  

&nbsp;  - Detect schema from raw CSV.  

&nbsp;  - Register in Glue Data Catalog.  



4\.   AWS Glue ETL (PySpark Job)  

&nbsp;  - Clean nulls, transform columns (e.g., date formats, derived columns).  

&nbsp;  - Save curated data back to S3 (Curated Zone).  



5\.   Amazon Athena  (Validation) 

&nbsp;  - Run SQL queries on curated patient data in S3.  



6\.   Amazon Redshift (Data Warehouse) 

&nbsp;  - Create tables and load curated data using COPY command.  



7\.   Amazon QuickSight (Visualization)

&nbsp;  - Build dashboards:  

&nbsp;    - Avg recovery days by city 

&nbsp;    - Recovery by age group  

&nbsp;    - Impact of diabetes/surgery type on recovery  



------



**Example Athena Query**



```sql

CREATE EXTERNAL TABLE patient\_recovery\_curated (

&nbsp;   patient\_id BIGINT,

&nbsp;   name STRING,

&nbsp;   age BIGINT,

&nbsp;   gender STRING,

&nbsp;   diabetes BIGINT,

&nbsp;   hypertension BIGINT,

&nbsp;   heart\_disease BIGINT,

&nbsp;   smoker\_status STRING,

&nbsp;   surgery\_type STRING,

&nbsp;   surgery\_date DATE,

&nbsp;   recovery\_days BIGINT,

&nbsp;   bmi DOUBLE,

&nbsp;   hospital STRING,

&nbsp;   city STRING,

&nbsp;   outcome STRING

)

STORED AS PARQUET

LOCATION 's3://patient-recovery-data-2025/curated/';



SELECT city, AVG(recovery\_days) AS avg\_recovery

FROM patient\_recovery\_curated

GROUP BY city

ORDER BY avg\_recovery DESC;





---



**Example Redshift Load**



sql

CREATE TABLE patient\_recovery (

&nbsp;   patient\_id BIGINT,

&nbsp;   name VARCHAR(100),

&nbsp;   age INT,

&nbsp;   gender VARCHAR(10),

&nbsp;   diabetes INT,

&nbsp;   hypertension INT,

&nbsp;   heart\_disease INT,

&nbsp;   smoker\_status VARCHAR(20),

&nbsp;   surgery\_type VARCHAR(50),

&nbsp;   surgery\_date DATE,

&nbsp;   recovery\_days INT,

&nbsp;   bmi FLOAT,

&nbsp;   hospital VARCHAR(200),

&nbsp;   city VARCHAR(50),

&nbsp;   outcome VARCHAR(50)

);



COPY patient\_recovery

FROM 's3://patient-recovery-data-2025/curated/'

IAM\_ROLE 'arn:aws:iam::your\_account\_id:role/YourRedshiftS3ReadRole'

FORMAT AS PARQUET;

```



---



**QuickSight Dashboards**



&nbsp; - Average recovery time by city  

&nbsp; - Recovery distribution by age group  

&nbsp; - Impact of diabetes on recovery days  

&nbsp; - Surgery type vs recovery outcome  



---



**Summary**



This project implements a Healthcare Data Lake \& ETL Pipeline on AWS.  

It shows how to ingest, clean, transform, query, and visualize healthcare data efficiently.





