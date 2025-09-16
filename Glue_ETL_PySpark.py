import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import to_date, col
from pyspark.sql.types import IntegerType, LongType, DoubleType

# Initialize contexts and job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read raw data from S3 as Glue DynamicFrame
raw_data_path = "s3://patient-recovery-data-2025/raw/patient_recovery_data.csv"
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": [raw_data_path], "recurse": True},
    transformation_ctx="raw_data"
)

# Convert DynamicFrame to DataFrame for transformations
df = dynamic_frame.toDF()

# Convert and cast columns explicitly for Redshift compatibility
df = df.withColumn("patient_id", col("patient_id").cast(LongType()))
df = df.withColumn("age", col("age").cast(IntegerType()))
df = df.withColumn("diabetes", col("diabetes").cast(IntegerType()))
df = df.withColumn("hypertension", col("hypertension").cast(IntegerType()))
df = df.withColumn("heart_disease", col("heart_disease").cast(IntegerType()))
df = df.withColumn("recovery_days", col("recovery_days").cast(IntegerType()))
df = df.withColumn("bmi", col("bmi").cast(DoubleType()))
df = df.withColumn("surgery_date", to_date(col("surgery_date"), "yyyy-MM-dd"))

# Optional: Drop rows with nulls in critical columns
df = df.na.drop(subset=["patient_id", "surgery_date"])

# Convert back to DynamicFrame
transformed_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "transformed_data")

# Write transformed data back to S3 curated zone in Parquet format
curated_data_path = "s3://patient-recovery-data-2025/curated/"
glueContext.write_dynamic_frame.from_options(
    frame=transformed_dynamic_frame,
    connection_type="s3",
    format="parquet",
    connection_options={"path": curated_data_path, "partitionKeys": []},
    transformation_ctx="write_curated"
)

job.commit()
