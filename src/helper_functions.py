import json
from src.constants import JSON_TYPE, XML_TYPE

def build_response(status_code, content_type, body):
    """Builds a response object to be returned by the lambda handler using the provided status code, content-type, and body.

    Args:
        status_code: int that indicates the status code of the operation
        content_type: str that indicates the media type of the data being passed through the body. Is of either JSON or XML type, as retrieved from constants.py
        body: str that indicates the message to be returned (raw XML string for XML_TYPE, or any value to be JSON-encoded for JSON_TYPE)

    Returns:
        Response: dict with statusCode, headers (Content-Type), and body.
        For XML_TYPE the body is the raw string; for JSON_TYPE the body is json.dumps(body).
    """

    if content_type == XML_TYPE:
        response_body = body if isinstance(body, str) else str(body)

    else:
        response_body = json.dumps(body)

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': content_type
        },
        'body': response_body
    }
