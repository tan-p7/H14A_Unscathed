# Import xml parsing module
import xml.etree.ElementTree as ET

# Import functions required for testing
from src.lambda_function import lambda_handler
from src.delete_despatch import delete_despatch_advice
from src.retrieve_despatch_by_id import get_despatch_advice_by_id
from src.generate_despatch import generate_despatch
from constants import order1, order2, order3

# Define namespaces used in UBL 2.4
namespaces = {
    'xmlns': 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2',
    'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
    'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
}

# General helper functions for the API
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


# Helper functions for testing code
def parse_despatch_advice_and_return_id(despatch_advice):
    """Parses a UBL XML despatch advice string and returns the despatch_id.

    Args:
        despatch_advice: XML string of the despatch advice to be parsed
    
    Returns: 
        despatch_id: int ID referring to the despatch advice
    """

    # Setup XML parsing for generated despatch advice document
    tree = ET.fromstring(despatch_advice)
    root = tree.getroot()

    # Find the despatch_id in the despatch advice
    despatch_id = root.find('cbc:ID', namespaces).text
    return int(despatch_id)

def parse_despatch_advice_and_return_success_boolean(despatch_advice):
    """Parses a potential despatch advice string and returns True if it is an XML string, and False if not

    Args:
        despatch_advice: XML string of the despatch advice to be parsed
    
    Returns: 
        boolean: True if the string is an XML string, and false if not
    """

    try:
        ET.fromstring(despatch_advice)
    except ET.ParseError:
        return False
    return True

def generate_three_despatch_advices_and_return_ids():
    """Generates three despatch advices and returns a list of IDs.

    Args:
        despatch_advice: XML string of the despatch advice to be parsed
    
    Returns: 
        despatch_ids: list of int IDs referring to the despatch advices
    """

    despatch_ids = []
    order_documents = [ order1, order2, order3 ]

    # Generate three despatch advices and retrieve their despatch_id
    for order in order_documents:
        generate_response = generate_despatch(order, {})
        despatch_advice = generate_response.get('xml', '')
        despatch_id = parse_despatch_advice_and_return_id(despatch_advice)
        despatch_ids.append(despatch_id)
    
    return despatch_ids
