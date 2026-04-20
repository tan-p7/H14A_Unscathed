# Import python modules needed for testing
import pytest
from unittest.mock import patch, MagicMock
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
            mock_table.query.side_effect = error

            response = retrieve_all_despatch_advice("user@example.com")
            mock_table.query.assert_called_once()
            assert response["statusCode"] == 503
            assert response["headers"]["Content-Type"] == "application/json"

    def test_successfully_retrieves_all_despatch_advice(self):
        # Existing despatch advices are wrapped in a DespatchAdviceList container.
        # Simulate a response for multiple despatch advice documents
        mock_dynamodb_response = [
            {"despatch_id": "1"},
            {"despatch_id": "2"}
        ]

        mock_s3_objects = {
            "dispatches/1.xml": b"<DespatchAdvice><ID>1</ID></DespatchAdvice>",
            "dispatches/2.xml": b"<DespatchAdvice><ID>2</ID></DespatchAdvice>"
        }

        with patch("src.db.dynamodb_table") as mock_table, \
             patch("src.s3.s3_client") as mock_s3_client, \
             patch("src.s3.BUCKET_NAME", "mock-bucket"):

            mock_table.query.return_value = {"Items": mock_dynamodb_response}

            def mock_get_object(Bucket, Key):
                return {"Body": MagicMock(read=lambda: mock_s3_objects[Key])}

            mock_s3_client.get_object.side_effect = mock_get_object

            response = retrieve_all_despatch_advice("user@example.com")

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
        mock_dynamodb_response = []

        with patch("src.db.dynamodb_table") as mock_table, \
             patch("src.s3.s3_client") as mock_s3_client, \
             patch("src.s3.BUCKET_NAME", "mock-bucket"):

            mock_table.query.return_value = {"Items": mock_dynamodb_response}

            # Try to retrieve non-existent despatch advice
            response = retrieve_all_despatch_advice("user@example.com")

            mock_table.query.assert_called_once()

        # Returns a 200 response with an empty DespatchAdviceList container.
        assert response["statusCode"] == 200
        assert response["headers"]["Content-Type"] == XML_TYPE
        body = response["body"]
        assert body.startswith("<DespatchAdviceList")
        assert body.endswith("</DespatchAdviceList>")
        # No inner DespatchAdvice documents when there are no items
        assert "<DespatchAdvice>" not in body