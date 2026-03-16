# Import python modules needed for testing
import pytest
from unittest.mock import patch
from botocore.exceptions import ClientError
from src.constants import XML_TYPE, JSON_TYPE

# Import function to test
from src.retrieve_all_despatch import retrieve_all_despatch_advice

class TestRetrieveAllDespatchAdvice:
    def test_retrieve_all_client_error(self):
        # Simulate a Client Error when accessing the table (Message required for e.response['Error']['Message'])
        error = ClientError(
            {
                "Error": {
                    "Code": "InternalServerError",
                    "Message": "DynamoDB scan failure"
                }
            },
            "Scan"
        )
        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.scan.side_effect = error

            response = retrieve_all_despatch_advice()
            mock_table.scan.assert_called_once()
            assert response["statusCode"] == 503
            assert response["headers"]["Content-Type"] == "application/json"

    def test_successfully_retrieves_all_despatch_advice(self):
        # Existing despatch advices are wrapped in a DespatchAdviceList container.
        # Simulate a response for multiple despatch advice documents
        mock_response = [
            {"despatch_ubl": "<DespatchAdvice><ID>1</ID></DespatchAdvice>"},
            {"despatch_ubl": "<DespatchAdvice><ID>2</ID></DespatchAdvice>"}
        ]

        with patch("src.db.dynamodb_table") as mock_table:
            # Retrieve all despatch advice documents
            mock_table.scan.return_value = {"Items": mock_response}
            response = retrieve_all_despatch_advice()

        # Check that the correct response was returned
        assert response["statusCode"] == 200
        assert response["headers"]["Content-Type"] == XML_TYPE
        body = response["body"]
        # Should be wrapped in a single DespatchAdviceList element
        assert body.startswith("<DespatchAdviceList")
        assert body.endswith("</DespatchAdviceList>")
        # Original documents should appear inside the wrapper
        assert "<DespatchAdvice><ID>1</ID></DespatchAdvice>" in body
        assert "<DespatchAdvice><ID>2</ID></DespatchAdvice>" in body

    def test_fails_to_retrieve_when_no_despatch_advice_exists(self):
        # Empty scan should still return an empty DespatchAdviceList container.
        mock_response = []

        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.scan.return_value = {"Items": mock_response}

            # Try to retrieve non-existent despatch advice
            response = retrieve_all_despatch_advice()

            mock_table.scan.assert_called_once()

        # Returns a 200 response with an empty DespatchAdviceList container.
        assert response["statusCode"] == 200
        assert response["headers"]["Content-Type"] == XML_TYPE
        body = response["body"]
        assert body.startswith("<DespatchAdviceList")
        assert body.endswith("</DespatchAdviceList>")
        # No inner DespatchAdvice documents when there are no items
        assert "<DespatchAdvice>" not in body

