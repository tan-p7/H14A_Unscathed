# Import python modules needed for testing
import pytest
from unittest.mock import patch
from botocore.exceptions import ClientError

# Import function to test
from src.delete_despatch import delete_despatch_advice

class TestDeleteDespatchAdvice:
    # Test that an existing despatch advice is successfully deleted
    def test_successfully_deletes_despatch_advice(self):
        # Simulate a response for the mock table
        mock_response = {
            "Attributes": {
                "despatchId": "123"
            }
        }

        with patch("src.db.dynamodb_table") as mock_table:
            # Delete the despatch advice
            mock_table.delete_item.return_value = mock_response
            response = delete_despatch_advice("123")

            # Ensure that the delete function was called once and works
            mock_table.delete_item.assert_called_once_with(
                Key={"despatchId": "123"},
                ReturnValues="ALL_OLD"
            )

            # Check that the correct response was returned
            assert response["statusCode"] == 204

    # Test that a non-existent despatch advice cannot be deleted
    def test_fails_to_delete_when_despatch_advice_does_not_exist(self):
        mock_response = {}

        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.delete_item.return_value = mock_response

            # Try to delete a non-existent despatch advice
            response = delete_despatch_advice("-100")
            assert response["statusCode"] == 404

    # Test that the deleting the table returns 503 when AWS throws a ClientError
    def test_delete_client_error(self):
        # Simulate a Client Error when accessing the table
        error = ClientError(
            {
                "Error": {
                    "Code": "InternalServerError",
                    "Message": "DynamoDB failure"
                }
            },
            "DeleteItem"
        )

        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.delete_item.side_effect = error

            # Ensure that the delete function was called once and works
            response = delete_despatch_advice("123")
            mock_table.delete_item.assert_called_once_with(
                Key={"despatchId": "123"},
                ReturnValues="ALL_OLD"
            )

            # Check that it fails to delete when AWS throws a client error
            assert response["statusCode"] == 503
