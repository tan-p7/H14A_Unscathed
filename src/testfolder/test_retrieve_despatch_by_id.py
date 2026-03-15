# Import python modules needed for testing
import pytest
from unittest.mock import patch
from botocore.exceptions import ClientError

# Import function to test
from src.retrieve_despatch_by_id import get_despatch_advice_by_id

class TestRetrieveDespatchAdviceById:
    # Test that an existing despatch advice is successfully retrieved
    def test_successfully_retrieves_despatch_advice(self):
        # Simulate a response for the mock table
        mock_response = {
            "Item": {
                "despatch_ubl": "<xml>sample document</xml>"
            }
        }

        with patch("src.db.dynamodb_table") as mock_table:
            # Retrieve the despatch advice
            mock_table.get_item.return_value = mock_response
            response = get_despatch_advice_by_id("123")

            # Ensure that the retrieve function was called once and works
            mock_table.get_item.assert_called_once_with(Key={"despatch_id": "123"})

            # Check that a 200 response was returned
            assert response["statusCode"] == 200
            assert response["headers"]["Content-Type"] == "application/xml"
            assert response["body"] == "<xml>sample document</xml>"

    # Test that a non-existent despatch advice cannot be retrieved
    def test_fails_to_retrieve_when_despatch_advice_does_not_exist(self):
        # Simulate item not found
        mock_response = {}

        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = mock_response

            # Try to retrieve a non-existent despatch advice
            response = get_despatch_advice_by_id("999")
            mock_table.get_item.assert_called_once_with(Key={"despatch_id": "999"})

            # Check that a 404 response was returned
            assert response["statusCode"] == 404
            assert response["headers"]["Content-Type"] == "application/json"

    # Test that the retrieving the table returns 503 when AWS throws a ClientError
    def test_retrieve_client_error(self):
        # Simulate a Client Error when accessing the table
        error = ClientError(
            {
                "Error": {
                    "Code": "InternalServerError",
                    "Message": "DynamoDB failure"
                }
            },
            "GetItem"
        )

        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.get_item.side_effect = error

            # Ensure that the retrieve function was called once and works
            response = get_despatch_advice_by_id("123")
            mock_table.get_item.assert_called_once_with(Key={"despatch_id": "123"})

            # Check that it fails to retrieve when AWS throws a client error
            assert response["statusCode"] == 503
            assert response["headers"]["Content-Type"] == "application/json"
