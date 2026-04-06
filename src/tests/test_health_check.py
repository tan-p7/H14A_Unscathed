import pytest
from unittest.mock import patch, PropertyMock
from botocore.exceptions import ClientError
from src.lambda_function import health_check

# Test that the health check returns 200 when the DynamoDB table is ACTIVE
class TestHealthCheckSuccess:
    def test_health_check_active(self):
        with patch('src.db.dynamodb_table') as mock_table:
            mock_table.table_status = 'ACTIVE'
            response = health_check({}, {})
            assert response['statusCode'] == 200


# Test that the health check returns 503 when the DynamoDB table is not ready
class TestHealthCheckTableNotReady:
    @pytest.mark.parametrize("status", ["CREATING", "UPDATING", "DELETING"])
    def test_health_check_not_ready(self, status):
        with patch('src.db.dynamodb_table') as mock_table:
            mock_table.table_status = status
            response = health_check({}, {})
            assert response['statusCode'] == 503


# Test that the health check returns 503 when AWS throws a ClientError
class TestHealthCheckErrors:
    def test_health_check_client_error(self):
        with patch('src.db.dynamodb_table') as mock_table:
            type(mock_table).table_status = PropertyMock(
                side_effect=ClientError(
                    {'Error': {'Code': '503', 'Message': 'AWS Error'}},
                    'RetrieveDespatch'
                )
            )
            response = health_check({}, {})
            assert response['statusCode'] == 503
