"""
Despatch ownership mapping table handle.

Table schema: PK email_id (S), SK despatch_id (S)
"""
import os
import boto3

_REGION = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
dynamodb = boto3.resource("dynamodb", region_name=_REGION)

DESPATCH_TABLE_NAME = os.environ.get("DESPATCH_TABLE_NAME", "despatch_id_email")

dynamodb_table = dynamodb.Table(DESPATCH_TABLE_NAME)