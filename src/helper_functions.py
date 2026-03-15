import json

def build_response(status_code, content_type, body):
    """Builds a JSON response object to be returned by the lambda handler using the provided status code, content-type, and body.

    Args:
        status_code: int that indicates the status code of the operation
        content_type: str that indicates the media type of the data being passed through the body. Is of either JSON or XML type, as retrieved from constants.py
        body: str that indicates the message to be returned
    
    Returns: 
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': content_type
        },
        'body': json.dumps(body)
    }
