def build_json_response(status_code, body):
    """Builds a JSON response object to be returned by the lambda handler using the provided status code and body. The data returned in the body is returned in JSON format.

    Args:
        status_code: int that indicates the status code of the operation
        body: str that indicates the message to be returned
    
    Returns: 
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': body
    }

def build_xml_response(status_code, body):
    """Builds an JSON response object to be returned by the lambda handler using the provided status code and body. The data returned in the body is returned in XML format. Used for returning despatch advice documents, which follow UBL XML format.

    Args:
        status_code: int that indicates the status code of the operation
        body: str that indicates the message to be returned
    
    Returns: 
        Response: JSON object structure detailing the statusCode, Content-Type, and body
    """
    
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/xml'
        },
        'body': body
    }