import pytest
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler


BASE_URL = '/api/despatch'
HEALTH_CHECK_PATH = BASE_URL + '/health'
DESPATCH_ADVICE_PATH = BASE_URL + '/despatch-advice'


def make_event(method, path, path_params=None, body=None, headers=None):
    event = {
        'httpMethod': method,
        'path': path,
        'pathParameters': path_params
    }
    if body is not None:
        event['body'] = body
    if headers is not None:
        event['headers'] = headers
    return event



class TestLambdaHealthCheckRoute:
    @patch('src.lambda_function.health_check')
    def test_get_health_check_routes_correctly(self, mock_health):
        mock_health.return_value = {'statusCode': 200}
        response = lambda_handler(make_event('GET', HEALTH_CHECK_PATH), {})
        mock_health.assert_called_once()
        assert response['statusCode'] == 200



class TestLambdaRetrieveAll:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_get_all_despatch_returns_response(self, mock_retrieve, _mock_auth):
        mock_retrieve.return_value = {'statusCode': 200}
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        mock_retrieve.assert_called_once_with("user@example.com")
        assert response['statusCode'] == 200


class TestLambdaGenerateDespatch:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.generate_despatch')
    def test_post_despatch_advice_calls_generate_with_body(self, mock_generate, _mock_auth):
        mock_generate.return_value = {'statusCode': 200}
        body = '<Order xmlns="urn:oasis:names:specification:ubl:schema:xsd:Order-2">...</Order>'
        response = lambda_handler(make_event('POST', DESPATCH_ADVICE_PATH, body=body), {})
        mock_generate.assert_called_once_with(body, "user@example.com")
        assert response['statusCode'] == 200

    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.generate_despatch')
    def test_post_despatch_advice_passes_empty_string_when_no_body(self, mock_generate, _mock_auth):
        mock_generate.return_value = {'statusCode': 400}
        response = lambda_handler(make_event('POST', DESPATCH_ADVICE_PATH), {})
        mock_generate.assert_called_once_with('', "user@example.com")
        assert response['statusCode'] == 400


class TestLambdaRetrieveDespatchById:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.retrieve_despatch')
    def test_get_despatch_by_id_calls_retrieve_with_despatch_id(self, mock_retrieve, _mock_auth):
        mock_retrieve.return_value = {'statusCode': 200}
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('GET', path, path_params={'despatch-id': '12345'}),
            {}
        )
        mock_retrieve.assert_called_once_with("user@example.com", '12345')
        assert response['statusCode'] == 200

    @patch('src.lambda_function.retrieve_despatch')
    def test_get_despatch_by_id_returns_404_when_despatch_id_missing(self, mock_retrieve):
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('GET', path, path_params={}),
            {}
        )
        mock_retrieve.assert_not_called()
        assert response['statusCode'] == 404


class TestLambdaUpdateDespatch:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.update_despatch_advice')
    def test_put_despatch_advice_calls_update_with_id_and_body(self, mock_update, _mock_auth):
        mock_update.return_value = {'statusCode': 200}
        path = DESPATCH_ADVICE_PATH + '/999'
        body = '{"deliveredQuantity": 5}'
        response = lambda_handler(
            make_event('PUT', path, path_params={'despatch-id': '999'}, body=body),
            {}
        )
        mock_update.assert_called_once_with("user@example.com", '999', body)
        assert response['statusCode'] == 200

    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.update_despatch_advice')
    def test_put_despatch_advice_passes_empty_json_when_no_body(self, mock_update, _mock_auth):
        mock_update.return_value = {'statusCode': 200}
        path = DESPATCH_ADVICE_PATH + '/999'
        response = lambda_handler(
            make_event('PUT', path, path_params={'despatch-id': '999'}),
            {}
        )
        mock_update.assert_called_once_with("user@example.com", '999', '{}')
        assert response['statusCode'] == 200

    @patch('src.lambda_function.update_despatch_advice')
    def test_put_despatch_returns_404_when_despatch_id_missing(self, mock_update):
        path = DESPATCH_ADVICE_PATH + '/999'
        response = lambda_handler(
            make_event('PUT', path, path_params={}),
            {}
        )
        mock_update.assert_not_called()
        assert response['statusCode'] == 404


class TestLambdaDeleteDespatch:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.delete_despatch')
    def test_delete_despatch_by_id_calls_delete_with_despatch_id(self, mock_delete, _mock_auth):
        mock_delete.return_value = {'statusCode': 204}
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('DELETE', path, path_params={'despatch-id': '12345'}),
            {}
        )
        mock_delete.assert_called_once_with("user@example.com", '12345')
        assert response['statusCode'] == 204

    @patch('src.lambda_function.delete_despatch')
    def test_delete_despatch_returns_404_when_despatch_id_missing(self, mock_delete):
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('DELETE', path, path_params={}),
            {}
        )
        mock_delete.assert_not_called()
        assert response['statusCode'] == 404


class TestLambdaNotFound:
    def test_unknown_method_returns_404(self):
        response = lambda_handler(make_event('POST', HEALTH_CHECK_PATH), {})
        assert response['statusCode'] == 404

    def test_unknown_path_returns_404(self):
        response = lambda_handler(make_event('GET', '/api/despatch/unknown'), {})
        assert response['statusCode'] == 404


class TestLambdaExceptionHandling:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_exception_returns_500(self, mock_retrieve, _mock_auth):
        mock_retrieve.side_effect = Exception('Unexpected error')
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        assert response['statusCode'] == 500


class TestLambdaAuthRoutes:
    @patch('src.lambda_function.register')
    def test_post_register_routes_to_register(self, mock_register):
        mock_register.return_value = {'statusCode': 201}
        response = lambda_handler(
            make_event('POST', '/api/auth/register', body='{}'),
            {}
        )
        mock_register.assert_called_once()
        assert response['statusCode'] == 201

    @patch('src.lambda_function.login')
    def test_post_login_routes_to_login(self, mock_login):
        mock_login.return_value = {'statusCode': 200}
        response = lambda_handler(
            make_event('POST', '/api/auth/login', body='{}'),
            {}
        )
        mock_login.assert_called_once()
        assert response['statusCode'] == 200

    @patch('src.lambda_function.logout')
    def test_post_logout_routes_to_logout(self, mock_logout):
        mock_logout.return_value = {'statusCode': 204}
        response = lambda_handler(
            make_event('POST', '/api/auth/logout'),
            {}
        )
        mock_logout.assert_called_once()
        assert response['statusCode'] == 204


class TestLambdaCorsOptions:
    def test_options_despatch_returns_204(self):
        response = lambda_handler(
            make_event('OPTIONS', DESPATCH_ADVICE_PATH),
            {}
        )
        assert response['statusCode'] == 204

    def test_options_auth_returns_204(self):
        response = lambda_handler(
            make_event('OPTIONS', '/api/auth/register'),
            {}
        )
        assert response['statusCode'] == 204


class TestLambdaDespatchRequiresAuth:
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_get_all_without_token_returns_401(self, mock_retrieve):
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        mock_retrieve.assert_not_called()
        assert response['statusCode'] == 401
