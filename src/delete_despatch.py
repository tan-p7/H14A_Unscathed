# Import required modules for the API
import json
import boto3
from src.db import dynamodb_table
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE


def delete_despatch_advice(despatch_id):
    """ Deletes the despatch advice with the corresponding despatch ID if the ID provided is valid.

    Args:
        despatch_id: int that indicates the corresponding ID of the despatch advice document to be deleted
    
    Returns: 
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """

    try:
        # Try delete the despatch advice using despatch_id
        response = dynamodb_table.delete_item(
            Key={'despatchId': despatch_id},
            ReturnValues='ALL_OLD'
        )

        # Return error message if despatch_id does not correspond to a despatch advice
        if 'Attributes' not in response:
            return build_response(404, JSON_TYPE, f'Despatch advice {despatch_id} not found')

        # Else return deletion confirmation message
        return build_response(204, JSON_TYPE, f'Despatch advice {despatch_id} was deleted successfully.')

    except ClientError as e:
        print('Error:', e)
        return build_response(400, JSON_TYPE, e.response['Error']['Message'])
