# Import modules needed for testing
import pytest
import sys
import json
from unittest.mock import patch, MagicMock, PropertyMock
from botocore.exceptions import ClientError

# Import functions required for testing
from src.lambda_function import lambda_handler
from src.constants import order1
from src.delete_despatch import delete_despatch_advice
from src.retrieve_despatch_by_id import get_despatch_advice_by_id
from src.generate_despatch import generate_despatch
from src.helper_functions import parse_despatch_advice_and_return_id, parse_despatch_advice_and_return_success_boolean, generate_three_despatch_advices_and_return_ids

# Initialise URL constants
LAMBDA_URL = ''
BASE_URL = LAMBDA_URL + '/api/despatch'
DESPATCH_ADVICE_PATH = BASE_URL + '/despatch-advice'

# Makes a mock database for testing
mock_db = MagicMock()
sys.modules['db'] = mock_db

# Test that an existing despatch advice is successfully deleted
def test_successfully_deletes_lone_despatch_advice():
    with patch('src.db.dynamodb_table') as mock_table:
        mock_table.table_status = 'ACTIVE'

        # Generate a despatch advice and check that a successful response was returned
        generate_response = generate_despatch(order1, {})
        assert generate_response.get("statusCode", '') == 200
        despatch_advice = generate_response.get('xml', '')
        despatch_id = parse_despatch_advice_and_return_id(despatch_advice)

        # Delete despatch advice
        delete_response = delete_despatch_advice(despatch_id)
        assert delete_response.get("statusCode", '') == 204
        assert delete_response.get("body", '') == f"Despatch advice {despatch_id} was deleted successfully."

        # Try (and fail) to retrieve deleted despatch advice
        retrieve_response = get_despatch_advice_by_id(despatch_id)
        assert retrieve_response.get("statusCode", '') == 404
        assert retrieve_response.get("body", '') == f"Despatch advice {despatch_id} not found"

# Test that one of many despatch advices is successfully deleted
def test_successfully_deletes_one_of_multiple_despatch_advices():
    with patch('src.db.dynamodb_table') as mock_table:
        mock_table.table_status = 'ACTIVE'

        # Generate three despatch advices
        despatch_ids = generate_three_despatch_advices_and_return_ids()

        # Delete the second despatch advice
        delete_response = delete_despatch_advice(despatch_ids[1])
        assert delete_response.get("statusCode", '') == 204
        assert delete_response.get("body", '') == f"Despatch advice {despatch_ids[1]} was deleted successfully."

        # Try (and fail) to retrieve deleted despatch advice
        retrieve_response = get_despatch_advice_by_id(despatch_ids[1])
        assert retrieve_response.get("statusCode", '') == 404
        assert retrieve_response.get("body", '') == f"Despatch advice {despatch_ids[1]} not found"

        # Successfully retrieve the other two despatch advices
        retrieve_response = get_despatch_advice_by_id(despatch_ids[0])
        assert retrieve_response.get("statusCode", '') == 200
        xml_string = retrieve_response.get("body", '')
        assert parse_despatch_advice_and_return_success_boolean(xml_string) == True

        retrieve_response = get_despatch_advice_by_id(despatch_ids[2])
        assert retrieve_response.get("statusCode", '') == 200
        xml_string = retrieve_response.get("body", '')
        assert parse_despatch_advice_and_return_success_boolean(xml_string) == True

# Test that multiple despatch advices are successfully deleted
def test_successfully_deletes_multiple_despatch_advices():
    with patch('src.db.dynamodb_table') as mock_table:
        mock_table.table_status = 'ACTIVE'

        # Generate three despatch advices
        despatch_ids = generate_three_despatch_advices_and_return_ids()

        # Delete the first and second despatch advices
        delete_response = delete_despatch_advice(despatch_ids[0])
        assert delete_response.get("statusCode", '') == 204
        assert delete_response.get("body", '') == f"Despatch advice {despatch_ids[0]} was deleted successfully."

        delete_response = delete_despatch_advice(despatch_ids[1])
        assert delete_response.get("statusCode", '') == 204
        assert delete_response.get("body", '') == f"Despatch advice {despatch_ids[1]} was deleted successfully."

        # Try (and fail) to retrieve deleted despatch advices
        retrieve_response = get_despatch_advice_by_id(despatch_ids[0])
        assert retrieve_response.get("statusCode", '') == 404
        assert retrieve_response.get("body", '') == f"Despatch advice {despatch_ids[0]} not found"

        retrieve_response = get_despatch_advice_by_id(despatch_ids[1])
        assert retrieve_response.get("statusCode", '') == 404
        assert retrieve_response.get("body", '') == f"Despatch advice {despatch_ids[1]} not found"

        # Successfully retrieve the remaining despatch advice
        retrieve_response = get_despatch_advice_by_id(despatch_ids[2])
        assert retrieve_response.get("statusCode", '') == 200
        xml_string = retrieve_response.get("body", '')
        assert parse_despatch_advice_and_return_success_boolean(xml_string) == True

# Test that a non-existent despatch advice cannot be deleted
def test_fails_to_delete_when_despatch_advice_does_not_exist():
    with patch('src.db.dynamodb_table') as mock_table:
        mock_table.table_status = 'ACTIVE'

        # Delete despatch advice
        delete_response = delete_despatch_advice(-100)
        assert delete_response.get("statusCode", '') == 404
        assert delete_response.get("body", '') == f"Despatch advice {despatch_id} not found"

# Test that not passing in a despatch_id returns an error
def test_fails_to_delete_despatch_advice_with_no_id():
    with patch('src.db.dynamodb_table') as mock_table:
        mock_table.table_status = 'ACTIVE'

        # Generate a despatch advice and check that a successful response was returned
        generate_response = generate_despatch(order1, {})
        assert generate_response.get("statusCode", '') == 200
        despatch_advice = generate_response.get('xml', '')

        # Create a API Gateway event for a delete request
        event = {
            "resource": LAMBDA_URL,
            "path": DESPATCH_ADVICE_PATH,
            "pathParameters": null,
            "httpMethod": "DELETE",
            "headers": { "Content-Type": "application/json" },
            "body": "",
            "isBase64Encoded": false
        }

        lambda_response = lambda_handler(event, {})
        assert lambda_response.get("statusCode", '') == 404
        assert lambda_response.get("body", '') == "Not Found"

# Test that passing in a non-integer despatch_id returns an error
def test_fails_to_delete_despatch_advice_with_non_digit_id():
    with patch('src.db.dynamodb_table') as mock_table:
        mock_table.table_status = 'ACTIVE'

        # Generate a despatch advice and check that a successful response was returned
        generate_response = generate_despatch(order1, {})
        assert generate_response.get("statusCode", '') == 200
        despatch_advice = generate_response.get('xml', '')

        # Create a API Gateway event for a delete request
        event = {
            "resource": LAMBDA_URL,
            "path": DESPATCH_ADVICE_PATH + '/a',
            "pathParameters": {
                "despatch-id": "a"
            },
            "httpMethod": "DELETE",
            "headers": { "Content-Type": "application/json" },
            "body": "",
            "isBase64Encoded": false
        }

        lambda_response = lambda_handler(event, {})
        assert lambda_response.get("statusCode", '') == 404
        assert lambda_response.get("body", '') == "Not Found"

# Test that the deleting the table returns 503 when AWS throws a ClientError
def test_fails_when_client_error_returned():
    with patch('src.lambda_function.dynamodb_table') as mock_table:
        type(mock_table).table_status = PropertyMock(side_effect = ClientError(
            {'Error': {'Code': '503', 'Message': 'AWS Error'}},'RetrieveUser'))

        delete_response = delete_despatch_advice(1)
        assert delete_response.get("statusCode", '') == 503
