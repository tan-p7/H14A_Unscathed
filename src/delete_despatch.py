# Import required modules for the API
import src.db
from botocore.exceptions import ClientError
import src.s3 as s3

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE


def delete_despatch(despatch_id):
    """ Deletes the despatch advice with the corresponding despatch ID if the ID provided is valid.

    Args:
        despatch_id: str that indicates the corresponding ID of the despatch advice document to be deleted

    Returns:
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """

    try:
        # Try to delete the despatch advice using despatch_id
        response = src.db.dynamodb_table.delete_item(
            Key={'despatch_id': despatch_id},
            ReturnValues='ALL_OLD'
        )

        # Return error message if despatch_id does not correspond to a despatch advice
        if 'Attributes' not in response:
            return build_response(404, JSON_TYPE, f'Despatch advice {despatch_id} not found')

        key = f"dispatches/{despatch_id}.xml"

        try:
            s3.s3_client.delete_object(
                Bucket=s3.BUCKET_NAME,
                Key=key
            )
        except ClientError as e:
            print('Error:', e)

        # Else return deletion confirmation message
        return build_response(204, JSON_TYPE, f'Despatch advice {despatch_id} was deleted successfully.')

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])