import pytest
import sys
import json
from unittest.mock import patch, MagicMock, PropertyMock
from botocore.exceptions import ClientError
from src.lambda_function import healthCheck

# Makes a mock database anytime db from the healthCheck function in lambda_function.py is called
mock_db = MagicMock()
sys.modules['db'] = mock_db

# Test that the health check returns 200 when the DynamoDB table is ACTIVE
def test_health_check_active():
    with patch('src.lambda_function.dynamodb_table') as mock_table:
        mock_table.table_status = 'ACTIVE'
        response = healthCheck({}, {})
        assert response['statusCode'] == 200


# Test that the health check returns 503 when the DynamoDB table is CREATING (not ready)
def test_health_check_creating():
    with patch('src.lambda_function.dynamodb_table') as mock_table:
        mock_table.table_status = 'CREATING'
        response = healthCheck({}, {})
        assert response['statusCode'] == 503

# Test that the health check returns 503 when the DynamoDB table is UPDATING (not ready)
def test_health_check_updating():
    with patch('src.lambda_function.dynamodb_table') as mock_table:
        mock_table.table_status = 'UPDATING'
        response = healthCheck({}, {})
        assert response['statusCode'] == 503


# Test that the health check returns 503 when the DynamoDB table is DELETING (not ready)
def test_health_check_deleting():
    with patch('src.lambda_function.dynamodb_table') as mock_table:
        mock_table.table_status = 'DELETING'
        response = healthCheck({}, {})
        assert response['statusCode'] == 503

# Test that the health check returns 503 when AWS throws a ClientError
def test_health_check_client_error():
    with patch('src.lambda_function.dynamodb_table') as mock_table:
        type(mock_table).table_status = PropertyMock(side_effect = ClientError(
            {'Error': {'Code': '500', 'Message': 'AWS Error'}},'RetrieveUser'))
        
        response = healthCheck({}, {})
        assert response['statusCode'] == 503

