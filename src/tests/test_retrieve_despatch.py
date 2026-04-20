# Import python modules needed for testing
import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

# Import function to test
from src.retrieve_despatch import retrieve_despatch

class TestRetrieveDespatchAdviceById:
    # Test that an existing despatch advice is successfully retrieved
    def test_successfully_retrieves_despatch_advice(self):
        # Simulate a response for the mock table
        mock_dynamodb_response = {"Item": {"despatch_id": "123"}}
        mock_s3_response = b"<xml>sample document</xml>"

        with patch("src.db.dynamodb_table") as mock_table, \
             patch("src.s3.s3_client") as mock_s3_client, \
             patch("src.s3.BUCKET_NAME", "mock-bucket"):

            mock_table.get_item.return_value = mock_dynamodb_response
            mock_s3_client.get_object.return_value = {"Body": MagicMock(read=lambda: mock_s3_response)}

            response = retrieve_despatch("user@example.com", "123")

            mock_table.get_item.assert_called_once_with(Key={"email_address": "user@example.com", "despatch_id": "123"})
            mock_s3_client.get_object.assert_called_once_with(
                Bucket="mock-bucket",
                Key="dispatches/123.xml"
            )

            # Check that a 200 response was returned
            assert response["statusCode"] == 200
            assert response["headers"]["Content-Type"] == "application/xml"
            assert response["body"] == "<xml>sample document</xml>"

    # Test that a non-existent despatch advice cannot be retrieved
    def test_fails_to_retrieve_when_despatch_advice_does_not_exist(self):
        # Simulate item not found
        mock_dynamodb_response = {}

        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = mock_dynamodb_response
            response = retrieve_despatch("user@example.com", "999")
            mock_table.get_item.assert_called_once_with(Key={"email_address": "user@example.com", "despatch_id": "999"})

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
            response = retrieve_despatch("user@example.com", "123")
            mock_table.get_item.assert_called_once_with(Key={"email_address": "user@example.com", "despatch_id": "123"})

            # Check that it fails to retrieve when AWS throws a client error
            assert response["statusCode"] == 503
            assert response["headers"]["Content-Type"] == "application/json"