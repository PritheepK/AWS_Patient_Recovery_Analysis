# Healthcare Data Lake & ETL Pipeline on AWS

This project demonstrates how to build a **Healthcare Data Lake and ETL Pipeline** using AWS services.  

The pipeline ingests raw patient recovery data, processes it with AWS Glue (PySpark), and makes it available for analytics in Redshift and visualization in QuickSight.

---

## Project Flow



1.Data Source (CSV)
  - Patient demographics, surgery info, recovery time.  

2.Amazon S3 (Raw Zone)  
  - Upload raw patient data.  

3.AWS Glue Crawler \& Data Catalog  
  - Detect schema from raw CSV.  
  - Register in Glue Data Catalog.  

4.AWS Glue ETL (PySpark Job)  
  - Clean nulls, transform columns (e.g., date formats, derived columns).  
  - Save curated data back to S3 (Curated Zone).  

5.Amazon Athena  (Validation) 
  - Run SQL queries on curated patient data in S3.  

6.Amazon Redshift (Data Warehouse) 
  - Create tables and load curated data using COPY command.  

7.Amazon QuickSight (Visualization)

   - Build dashboards:  
   - Avg recovery days by city 
   - Recovery by age group  
   - Impact of diabetes/surgery type on recovery  
------



## Example Athena Query


``````sql
CREATE EXTERNAL TABLE patient\_recovery\_curated (
    patient_id BIGINT,
    name STRING,
    age BIGINT,
    gender STRING,
    diabetes BIGINT,
    hypertension BIGINT,
    heart_disease BIGINT,
    smoker_status STRING,
    surgery_type STRING,
    surgery_date DATE,
    recovery_days BIGINT,
    bmi DOUBLE,
    hospital STRING,
    city STRING,
    outcome STRING
)
STORED AS PARQUET
LOCATION 's3://patient-recovery-data-2025/curated/';



SELECT city, AVG(recovery_days) AS avg_recovery
FROM patient_recovery_curated
GROUP BY city
ORDER BY avg_recovery DESC;
---

Example Redshift Load


```sql
CREATE TABLE patient_recovery (
    patient_id BIGINT,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    diabetes INT,
    hypertension INT,
    heart_disease INT,
    smoker_status VARCHAR(20),
    surgery_type VARCHAR(50),
    surgery_date DATE,
    recovery_days INT,
    bmi FLOAT,
    hospital VARCHAR(200),
    city VARCHAR(50),
    outcome VARCHAR(50)
);


COPY patient_recovery
FROM 's3://patient-recovery-data-2025/curated/'
IAM_ROLE 'arn:aws:iam::your_account_id:role/RedshiftS3ReadRole'
FORMAT AS PARQUET;

---

## QuickSight Dashboards

  - Average recovery time by city  

  - Recovery distribution by age group  

  - Impact of diabetes on recovery days  

  - Surgery type vs recovery outcome  

---

## Summary

This project implements a Healthcare Data Lake \& ETL Pipeline on AWS.  
It shows how to ingest, clean, transform, query, and visualize healthcare data efficiently.





