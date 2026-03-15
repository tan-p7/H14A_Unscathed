import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
dynamodb_table = dynamodb.Table('Despatch-Advices')