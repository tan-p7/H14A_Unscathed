import json
import boto3
from db import dynamodb_table

# Import functions and constants that perform the core data processing
from helper_functions import build_response
from constants import JSON_TYPE

# Initialise URL constants
BASE_URL = '/api/despatch'
HEALTH_CHECK_PATH = BASE_URL + '/health'

def lambda_handler(event, context):
  http_method = event.get('httpMethod')
  path = event.get('path')
  if http_method == 'GET' and path == HEALTH_CHECK_PATH:
    try:
      dynamodb_table.table_status #FIXXXXXXX
      response = build_response(200, JSON_TYPE, 'Service is operational')

    except Exception as e:
      print('Error:', e)
      response = build_response(400, JSON_TYPE, 'Error processing request')
    return response
