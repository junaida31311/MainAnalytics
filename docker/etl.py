import boto3
import psycopg2
import json
import os

# AWS Clients
s3 = boto3.client("s3")
glue = boto3.client("glue")

# Environment Variables
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")
RDS_HOST = os.getenv("RDS_HOST")
RDS_PORT = os.getenv("RDS_PORT", 5432)
RDS_DB = os.getenv("RDS_DB")
RDS_USER = os.getenv("RDS_USER")
RDS_PASS = os.getenv("RDS_PASS")
GLUE_DATABASE = os.getenv("GLUE_DATABASE")
GLUE_TABLE = os.getenv("GLUE_TABLE")

def fetch_s3_data():
    response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    return json.loads(response['Body'].read().decode('utf-8'))

def push_to_rds(data):
    try:
        conn = psycopg2.connect(
            host=RDS_HOST, port=RDS_PORT, database=RDS_DB,
            user=RDS_USER, password=RDS_PASS
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO your_table (data) VALUES (%s)", (json.dumps(data),))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted into RDS successfully")
    except Exception as e:
        print(f"RDS failed: {e}")
        push_to_glue(data)

def push_to_glue(data):
    response = glue.create_table(
        DatabaseName=GLUE_DATABASE,
        TableInput={
            'Name': GLUE_TABLE,
            'StorageDescriptor': {
                'Columns': [{'Name': 'data', 'Type': 'string'}],
                'Location': f"s3://{S3_BUCKET}/glue/",
                'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            }
        }
    )
    print("Data stored in AWS Glue:", response)

def lambda_handler(event, context):
    data = fetch_s3_data()
    push_to_rds(data)

if __name__ == "_main_":
    lambda_handler({}, {})