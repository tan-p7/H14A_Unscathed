# Import required modules for the API
import json
from botocore.exceptions import ClientError

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE
import src.db

# Namespaces 
NS_UBL = 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2'
NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'

def retrieve_all_despatch_advice():
    """ Retrieves all saved despatch advice documents. 

    Returns: 
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """

    try: 
        # Scan all stored despatch advice documents
        response = src.db.dynamodb_table.scan()

        # Get the items from the response
        items = response.get('Items', [])

        # Extract the stored documents
        despatch_documents = [item['despatch_ubl'] for item in items]

        # Wrap them in a single UBL container
        all_despatches = (
            f'<DespatchAdviceList xmlns="{NS_UBL}" '
            f'xmlns:cbc="{NS_CBC}" '
            f'xmlns:cac="{NS_CAC}">'
            + "".join(despatch_documents) +
            '</DespatchAdviceList>'
        )

        return build_response(200, XML_TYPE, all_despatches)

    except ClientError as e:
        print('Error:', e)
        response = build_response(503, JSON_TYPE, 'Error processing request')
    return response

