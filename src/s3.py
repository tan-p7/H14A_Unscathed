import boto3
BUCKET_NAME = 'xml-storage-bucket'

## s3 client definition
s3_client = boto3.client("s3", region_name='us-east-1');
