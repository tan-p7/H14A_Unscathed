# Import required modules for the API
from botocore.exceptions import ClientError
import src.s3 as s3

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE
import src.db
from boto3.dynamodb.conditions import Key

# Namespaces 
NS_UBL = 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2'
NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'

def retrieve_all_despatch_advice(email_id: str):
    """ Retrieves all saved despatch advice documents.

    Returns:
        Response: dict with statusCode, headers, and body (XML)
    """

    try:
        # Query all despatch ids for this user (email_id partition key)
        response = src.db.dynamodb_table.query(
            KeyConditionExpression=Key("email_address").eq(email_id)
        )

        # Get the items from the response
        items = response.get('Items', [])

        despatch_documents = []

        for item in items:
            despatch_id = item["despatch_id"]
            key = f"dispatches/{despatch_id}.xml"

            try:
                s3_response = s3.s3_client.get_object(
                    Bucket=s3.BUCKET_NAME,
                    Key=key
                )
                xml_string = s3_response['Body'].read().decode('utf-8')
                despatch_documents.append(xml_string)
            except ClientError as e:
                print('Error:', e)

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
        response = build_response(503, JSON_TYPE, e.response['Error']['Message'])
    return response