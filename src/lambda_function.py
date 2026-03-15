# Import required modules for the API
import json
import boto3
import src.db
from botocore.exceptions import ClientError

# Import functions and constants that perform the core data processing
from src.helper_functions import build_response
from src.constants import JSON_TYPE
from src.delete_despatch import delete_despatch
from src.retrieve_despatch import retrieve_despatch
from src.generate_despatch import generate_despatch
from src.retrieve_all_despatch import retrieve_all_despatch_advice
from src.generate_despatch import generate_despatch

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
        path_parameters = event.get('pathParameters')
        
        # Determine the API endpoint requested and call the appropriate function 
        if http_method == 'GET' and path == HEALTH_CHECK_PATH:
            return healthCheck()
        
            return health_check(event, context)
        elif http_method == 'POST' and path == DESPATCH_ADVICE_PATH:
            return generate_despatch(event, context)
        elif http_method == 'GET' and path == DESPATCH_ADVICE_PATH:
            response = retrieve_all_despatch_advice()
        elif http_method == 'GET' and path.startswith(DESPATCH_ADVICE_PATH) and path_parameters:
            despatch_id = event['pathParameters'].get('despatch-id')

            # Validate despatch_id is provided and non-empty
            if not despatch_id:
                response = build_response(404, JSON_TYPE, "Not Found")
            else:
                # Pass through as string to match DynamoDB partition key type
                response = retrieve_despatch(despatch_id)
        elif http_method == 'DELETE' and path.startswith(DESPATCH_ADVICE_PATH) and path_parameters:
            despatch_id = event['pathParameters'].get('despatch-id')

            # Validate despatch_id is provided and non-empty
            if not despatch_id:
                response = build_response(404, JSON_TYPE, "Not Found")
            else:
                # Pass through as string to match DynamoDB partition key type
                response = delete_despatch(despatch_id)
        else:
            response = build_response(404, JSON_TYPE, 'Not Found')
        
    # Handle any errors raised accordingly
    except Exception as e:
        print('Error:', e)
        response = build_response(500, JSON_TYPE, 'Server error: Error processing request')
   
    return response



def health_check(event, context):
    """Handles health check requests from API Gateway by verifying that the service and DynamoDB table are operational.
    Args:
        Event: JSON-formatted data structure sent by API Gateway that contains request
               information such as the HTTP method and request path.
        Context: Object that provides runtime information about the function

    Returns:
        Response: JSON object structure containing the HTTP statusCode, Content-Type,
                  and body message.
    """
    try:
        status = src.db.dynamodb_table.table_status
        if status == 'ACTIVE':
            response = build_response(200, JSON_TYPE, 'Service is operational')
        else:
            response = build_response(503, JSON_TYPE, 'Table not ready')
    except ClientError as e:
        print('Error:', e)
        response = build_response(503, JSON_TYPE, e.response['Error']['Message'])
    return response
