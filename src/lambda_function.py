# Import required modules for the API
import src.db
from botocore.exceptions import ClientError

# Import functions and constants that perform the core data processing
from src.helper_functions import build_response
from src.constants import JSON_TYPE, ORDER_URL
from src.delete_despatch import delete_despatch
from src.retrieve_despatch import retrieve_despatch
from src.generate_despatch import generate_despatch
from src.retrieve_all_despatch import retrieve_all_despatch_advice
from src.update_despatch import update_despatch_advice
from src.auth_service import register, login, logout
from src.auth_dependencies import get_auth_context
from src.shopping_cart import addItemToShoppingCart, removeItemFromShoppingCart, updateItemInShoppingCart, retrieveShoppingCart, clearShoppingCart
from src.order_handling import createOrder, retrieveOrderById, updateOrder, deleteOrder

# Initialise URL constants
BASE_URL = '/api/despatch'
HEALTH_CHECK_PATH = BASE_URL + '/health'
DESPATCH_ADVICE_PATH = BASE_URL + '/despatch-advice'

AUTH_BASE = '/api/auth'
AUTH_REGISTER_PATH = AUTH_BASE + '/register'
AUTH_LOGIN_PATH = AUTH_BASE + '/login'
AUTH_LOGOUT_PATH = AUTH_BASE + '/logout'


def _auth_error_response(message: str):
    return build_response(401, JSON_TYPE, {"message": message})


def _require_auth(event):
    """Returns (claims, response). If response is not None, caller should return it."""
    claims, err = get_auth_context(event)
    if err:
        return None, _auth_error_response(err)
    return claims, None


def lambda_handler(event, context):
    """Handles requests coming from API Gateway and calls the appropriate route to manage despatch advices stored in the DynamoDB table.

    Args:
        Event: JSON-formatted data structure that triggers the Lambda function to run
        Context: Object that provides runtime information about the function

    Returns:
        Response: Response dict with statusCode, headers, and body
    """

    try:
        # Get information relevant to the http request
        http_method = event.get('httpMethod')
        path = event.get('path')
        path_parameters = event.get('pathParameters')        

        # CORS preflight (browser SPA)
        if http_method == 'OPTIONS' and (
            path.startswith(AUTH_BASE) or path.startswith(BASE_URL)
        ):
            return build_response(204, JSON_TYPE, "")

        # Auth routes (public)
        if http_method == 'POST' and path == AUTH_REGISTER_PATH:
            return register(event)
        if http_method == 'POST' and path == AUTH_LOGIN_PATH:
            return login(event)
        if http_method == 'POST' and path == AUTH_LOGOUT_PATH:
            return logout(event)

        # Determine the API endpoint requested and call the appropriate function
        if http_method == 'GET' and path == HEALTH_CHECK_PATH:
            return health_check(event, context)
        elif http_method == 'POST' and path == DESPATCH_ADVICE_PATH:
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                body = event.get('body') or ''
                response = generate_despatch(body, claims.get("email"))
        elif http_method == 'GET' and path == DESPATCH_ADVICE_PATH:
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                response = retrieve_all_despatch_advice(claims.get("email"))
        elif http_method == 'GET' and path.startswith(DESPATCH_ADVICE_PATH) and path_parameters:
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                despatch_id = event['pathParameters'].get('despatch-id')

                # Validate despatch_id is provided and non-empty
                if not despatch_id:
                    response = build_response(404, JSON_TYPE, "Not Found")
                else:
                    # Pass through as string to match DynamoDB partition key type
                    response = retrieve_despatch(claims.get("email"), despatch_id)
        elif http_method == 'PUT' and path.startswith(DESPATCH_ADVICE_PATH) and path_parameters:
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                despatch_id = event['pathParameters'].get('despatch-id')
                body = event.get('body') or '{}'

                if not despatch_id:
                    response = build_response(404, JSON_TYPE, "Not Found")
                else:
                    response = update_despatch_advice(claims.get("email"), despatch_id, body)
        elif http_method == 'DELETE' and path.startswith(DESPATCH_ADVICE_PATH) and path_parameters:
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                despatch_id = event['pathParameters'].get('despatch-id')

                if not despatch_id:
                    response = build_response(404, JSON_TYPE, "Not Found")
                else:
                    response = delete_despatch(claims.get("email"), despatch_id)
        elif http_method == 'GET' and path == '/':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': swagger_ui()
            }
        elif http_method == 'POST' and path == '/api/cart/items':
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                body = event.get('body') or '{}'
                response = addItemToShoppingCart(body)
        elif http_method == 'DELETE' and path.startsWith('/api/cart/items/'):
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                item_id = event['pathParameters'].get('item-id')
                response = removeItemFromShoppingCart(item_id)
        elif http_method == 'PUT' and path.startsWith('/api/cart/items/'):
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                item_id = event['pathParameters'].get('item-id')
                quantity = (body.get("quantity", ""))
                response = updateItemInShoppingCart(item_id, quantity)
        elif http_method == 'GET' and path == '/api/cart':
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                response = retrieveShoppingCart()
        elif http_method == 'DELETE' and path == '/api/cart':
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                response = clearShoppingCart()
        elif http_method == 'POST' and path == '/api/order':
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                response = createOrder()
        elif http_method == 'GET' and path.startsWith('/api/order/'):
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                order_id = event['pathParameters'].get('order-id')
                response = retrieveOrderById(order_id)
        elif http_method == 'PUT' and path.startsWith('/api/order/'):
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                body = event.get('body') or '{}'
                order_id = event['pathParameters'].get('order-id')
                response = updateOrder(order_id, body)
        elif http_method == 'DELETE' and path.startsWith('/api/order/'):
            claims, blocked = _require_auth(event)
            if blocked:
                response = blocked
            else:
                order_id = event['pathParameters'].get('order-id')
                response = deleteOrder(order_id)
        else:
            response = build_response(404, JSON_TYPE, 'Not Found')

    # Handle any errors raised accordingly
    except Exception as e:
        print('Error:', e)
        response = build_response(500, JSON_TYPE, 'Server error: Error processing request')

    return response

def swagger_ui():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Despatch Advice API - Docs</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
<script>
    SwaggerUIBundle({
        url: "https://api.swaggerhub.com/apis/unsw-7ef/Unscathed_Despatch_API/1.0.0/swagger.json",
        dom_id: '#swagger-ui',
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
        layout: "BaseLayout"
    })
</script>
</body>
</html>"""




def health_check(event, context):
    """Handles health check requests from API Gateway by verifying that the service and DynamoDB table are operational.
    Args:
        Event: JSON-formatted data structure sent by API Gateway that contains request
               information such as the HTTP method and request path.
        Context: Object that provides runtime information about the function

    Returns:
        Response: JSON object structure containing the HTTP statusCode, Content-Type,
                  and body message.
    """

    try:
        status = src.db.dynamodb_table.table_status
        if status == 'ACTIVE':
            response = build_response(200, JSON_TYPE, 'Service is operational')
        else:
            response = build_response(503, JSON_TYPE, 'Table not ready')
    except ClientError as e:
        print('Error:', e)
        response = build_response(503, JSON_TYPE, e.response['Error']['Message'])
    return response
