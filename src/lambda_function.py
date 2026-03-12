# Import required modules for the API
import json
import boto3
from botocore.exceptions import ClientError

# Import functions and constants that perform the core data processing
from helper_functions import build_response
from constants import JSON_TYPE
from delete_despatch import delete_despatch_advice

# Initialise URL constants
BASE_URL = '/api/despatch'
HEALTH_CHECK_PATH = BASE_URL + '/health'
DESPATCH_ADVICE_PATH = BASE_URL + '/despatch-advice'

def lambda_handler(event, context):
    """Handles requests coming from API Gateway and calls the appropriate route to manage despatch advices stored in the DynamoDB table.
    
    Args:
        Event: JSON-formatted data structure that triggers the Lambda function to run
        Context: Object that provides runtime information about the function

    Returns:
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """

    print('Request event: ', event)
    response = None
    
    try:
        # Get information relevant to the http request
        http_method = event.get('httpMethod')
        path = event.get('path')
        pathParameters = event.get('pathParameters')

        # Determine the API endpoint requested and call the appropriate function 
        if http_method == 'DELETE' and path.startswith(DESPATCH_ADVICE_PATH) and pathParameters:
            despatch_id = event['pathParameters'].get('despatch_id')

            # Validate despatch_id is provided
            if not despatch_id:
                response = build_response(404, JSON_TYPE, "Not Found")
            else:
                response = delete_despatch_advice(despatch_id)
        else:
            response = build_response(404, JSON_TYPE, 'Not Found')
        
    # Handle any errors raised accordingly
    except Exception as e:
        print('Error:', e)
        response = build_response(400, JSON_TYPE, 'Error processing request')
   
    return response
