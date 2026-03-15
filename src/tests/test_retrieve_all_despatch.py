# Import python modules needed for testing
import pytest
from unittest.mock import patch
from botocore.exceptions import ClientError
from src.constants import XML_TYPE, JSON_TYPE

# Import function to test
from src.retrieve_all_despatch import retrieve_all_despatch_advice

class TestRetrieveAllDespatchAdvice:
    # Test that an existing despatch advice is successfully retrieved 
    def test_successfully_retrieves_all_despatch_advice(self):
        #Simulate a response for multiple despatch advice documents
        mock_response = [
            {"despatch_ubl": "<DespatchAdvice><ID>1</ID></DespatchAdvice>"},
            {"despatch_ubl": "<DespatchAdvice><ID>2</ID></DespatchAdvice>"}
        ]

        combined_ubl = "<DespatchAdviceList>" + "".join([item["despatch_ubl"] for item in mock_response]) + "</DespatchAdviceList>"

        with patch("src.db.dynamodb_table") as mock_table:
            #Retrieve all despatch advice documents 
            mock_table.scan.return_value = {"Items": mock_response}
            response  = retrieve_all_despatch_advice()


            #Check that the correct response was returned
            assert response["statusCode"] == 200
            assert response["body"] == combined_ubl

    def test_fails_to_retrieve_when_no_despatch_advice_exists(self):
        mock_response = []
        combined_ubl = "<DespatchAdviceList>" + "".join([item["despatch_ubl"] for item in mock_response]) + "</DespatchAdviceList>"

        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.scan.return_value = {"Items": mock_response}

            # Try to retrieve non-existent despatch advice
            response = retrieve_all_despatch_advice()

            mock_table.scan.assert_called_once()

            # returns 
            assert response["statusCode"] == 200
            assert response["body"] == combined_ubl

    def test_retrieve_all_client_error(self):
        error = ClientError({"Error": {"Code": "InternalError"}}, "Scan")
        with patch("src.db.dynamodb_table") as mock_table:
            mock_table.scan.side_effect = error

            response = retrieve_all_despatch_advice()
            mock_table.scan.assert_called_once()
            assert response["statusCode"] == 503