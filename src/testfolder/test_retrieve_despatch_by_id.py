# TODO: mock dynamodb table, check passing correctly into generate_despatch and update despatch (string or obj?)
# Potential issues: Module imports not working

# Import python modules
import pytest

# Import functions required for testing
from src.constants import updated_order
from src.helper_functions import parse_despatch_advice_and_return_success_boolean, generate_despatch_advice_and_return_id
from src.delete_despatch import delete_despatch_advice
from src.retrieve_despatch_by_id import get_despatch_advice_by_id
from src.generate_despatch import generate_despatch
from src.update_despatch import update_despatch
# COME BACK: will need to match Tanishka's naming


# Unit/integration testing
def test_successfully_retrieves_despatch_advice():
    # Generate a despatch advice
    despatch_id = generate_despatch_advice_and_return_id()

    # Retrieve the despatch advice and check response is correct
    retrieve_response = get_despatch_advice_by_id(despatch_id)
    assert retrieve_response.get("statusCode", '') == 200
    xml_string = retrieve_response.get("body", '')
    assert parse_despatch_advice_and_return_success_boolean(xml_string) == True

def test_successfully_retrieves_updated_despatch_advice():
    # Generate and update a despatch advice
    despatch_id = generate_despatch_advice_and_return_id()
    update_despatch(despatch_id, updated_order)

    # Retrieve the despatch advice and check response is correct
    retrieve_response = get_despatch_advice_by_id(despatch_id)
    assert retrieve_response.get("statusCode", '') == 200
    xml_string = retrieve_response.get("body", '')
    assert parse_despatch_advice_and_return_success_boolean(xml_string) == True

def test_fails_to_retrieve_deleted_despatch_advice():
    # Generate a despatch advice
    despatch_id = generate_despatch_advice_and_return_id()

    # Delete the despatch advice
    delete_despatch_advice(despatch_id)

    # Retrieve the despatch advice and check response is correct
    retrieve_response = get_despatch_advice_by_id(despatch_id)
    assert retrieve_response.get("statusCode", '') == 404
    assert retrieve_response.get("body", '') == f"Despatch advice {despatch_id} not found"

def test_fails_to_retrieve_non_existent_despatch_advice():
    retrieve_response = get_despatch_advice_by_id(-100)
    assert retrieve_response.get("statusCode", '') == 404
    assert retrieve_response.get("body", '') == f"Despatch advice {despatch_id} not found"
