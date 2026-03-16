# Import required modules for the API
from botocore.exceptions import ClientError

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE
import src.db

def retrieve_despatch(despatch_id):
    """ Retrieves the despatch advice with the corresponding despatch ID if the ID provided is valid.

    Args:
        despatch_id: str that indicates the corresponding ID of the despatch advice document to be retrieved    

    Returns:
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """

    try:
        # Try to retrieve the despatch advice using despatch_id
        response = src.db.dynamodb_table.get_item(Key={'despatch_id': despatch_id})

        # Return error if despatch advice does not exist
        if 'Item' not in response:
            return build_response(404, JSON_TYPE, f'Despatch advice {despatch_id} not found')

        # Else return the despatch advice document
        return build_response(200, XML_TYPE, response['Item']['despatch_ubl']) 

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
