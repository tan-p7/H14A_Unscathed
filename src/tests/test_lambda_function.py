import pytest
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler


BASE_URL = '/api/despatch'
HEALTH_CHECK_PATH = BASE_URL + '/health'
DESPATCH_ADVICE_PATH = BASE_URL + '/despatch-advice'


def make_event(method, path, path_params=None):
    return {
        'httpMethod': method,
        'path': path,
        'pathParameters': path_params
    }



class TestLambdaHealthCheckRoute:
    @patch('src.lambda_function.health_check')
    def test_get_health_check_routes_correctly(self, mock_health):
        mock_health.return_value = {'statusCode': 200}
        response = lambda_handler(make_event('GET', HEALTH_CHECK_PATH), {})
        mock_health.assert_called_once()
        assert response['statusCode'] == 200



class TestLambdaRetrieveAll:
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_get_all_despatch_returns_response(self, mock_retrieve):
        mock_retrieve.return_value = {'statusCode': 200}
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        mock_retrieve.assert_called_once()
        assert response['statusCode'] == 200




class TestLambdaExceptionHandling:
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_exception_returns_500(self, mock_retrieve):
        mock_retrieve.side_effect = Exception('Unexpected error')
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        assert response['statusCode'] == 500