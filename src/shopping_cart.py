# Import required modules for the API
from botocore.exceptions import ClientError
import requests

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE, ORDER_URL
from src.auth_dependencies import extract_order_access_token, extract_order_refresh_token

def addItemToShoppingCart(event):
    try:
        body = event.get('body') or '{}'
        orderAccessToken = extract_order_access_token(event)
        orderRefreshToken = extract_order_refresh_token(event)
        refreshBody = { "refreshToken": orderRefreshToken }
        refreshResponse = requests.post(f"{ORDER_URL}/auth/refresh", json=refreshBody)

        if refreshResponse.status_code != 200:
            email = (body.get("email") or "").strip().lower()
            password = body.get("password") or ""

            reloginBody = {
                "email": email,
                "password": password
            }
            reloginResponse = requests.post(f"{ORDER_URL}/auth/login", json=reloginBody)
            if reloginResponse.status_code != 200:
                return build_response(503, JSON_TYPE, "Error occurred. Please login again.")
            else:
                orderAccessToken = reloginResponse.json.accessToken
                orderRefreshToken = reloginResponse.json.refreshToken
        else:
            orderAccessToken = refreshResponse.json.accessToken
            orderRefreshToken = refreshResponse.json.refreshToken

        item = {
            "itemId": body.get("itemId", ""),
            "quantity": int(body.get("quantity", ""))
        }

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }
    
        addToCartResponse = requests.post(f"{ORDER_URL}/cart/items", json=item, headers=headers)
        return build_response(addToCartResponse.status_code, JSON_TYPE, addToCartResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def removeItemFromShoppingCart(event):
    try:
        body = event.get('body') or '{}'
        orderAccessToken = extract_order_access_token(event)
        orderRefreshToken = extract_order_refresh_token(event)
        refreshBody = { "refreshToken": orderRefreshToken }
        refreshResponse = requests.post(f"{ORDER_URL}/auth/refresh", json=refreshBody)

        if refreshResponse.status_code != 200:
            email = (body.get("email") or "").strip().lower()
            password = body.get("password") or ""

            reloginBody = {
                "email": email,
                "password": password
            }
            reloginResponse = requests.post(f"{ORDER_URL}/auth/login", json=reloginBody)
            if reloginResponse.status_code != 200:
                return build_response(503, JSON_TYPE, "Error occurred. Please login again.")
            else:
                orderAccessToken = reloginResponse.json.accessToken
                orderRefreshToken = reloginResponse.json.refreshToken
        else:
            orderAccessToken = refreshResponse.json.accessToken
            orderRefreshToken = refreshResponse.json.refreshToken

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }
    
        itemId = event['pathParameters'].get('item-id')
        removeFromCartResponse = requests.delete(f"{ORDER_URL}/cart/items/{itemId}", headers=headers)
        return build_response(removeFromCartResponse.status_code, JSON_TYPE, removeFromCartResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def updateItemInShoppingCart(event):
    try:
        body = event.get('body') or '{}'
        orderAccessToken = extract_order_access_token(event)
        orderRefreshToken = extract_order_refresh_token(event)
        refreshBody = { "refreshToken": orderRefreshToken }
        refreshResponse = requests.post(f"{ORDER_URL}/auth/refresh", json=refreshBody)

        if refreshResponse.status_code != 200:
            email = (body.get("email") or "").strip().lower()
            password = body.get("password") or ""

            reloginBody = {
                "email": email,
                "password": password
            }
            reloginResponse = requests.post(f"{ORDER_URL}/auth/login", json=reloginBody)
            if reloginResponse.status_code != 200:
                return build_response(503, JSON_TYPE, "Error occurred. Please login again.")
            else:
                orderAccessToken = reloginResponse.json.accessToken
                orderRefreshToken = reloginResponse.json.refreshToken
        else:
            orderAccessToken = refreshResponse.json.accessToken
            orderRefreshToken = refreshResponse.json.refreshToken

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        itemId = event['pathParameters'].get('item-id')
        quantity = (body.get("quantity") or "")
        updateCartResponse = requests.update(f"{ORDER_URL}/cart/items/{itemId}", json={ "quantity": quantity }, headers=headers)
        return build_response(updateCartResponse.status_code, JSON_TYPE, updateCartResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def retrieveShoppingCart(event):
    try:
        body = event.get('body') or '{}'
        orderAccessToken = extract_order_access_token(event)
        orderRefreshToken = extract_order_refresh_token(event)
        refreshBody = { "refreshToken": orderRefreshToken }
        refreshResponse = requests.post(f"{ORDER_URL}/auth/refresh", json=refreshBody)

        if refreshResponse.status_code != 200:
            email = (body.get("email") or "").strip().lower()
            password = body.get("password") or ""

            reloginBody = {
                "email": email,
                "password": password
            }
            reloginResponse = requests.post(f"{ORDER_URL}/auth/login", json=reloginBody)
            if reloginResponse.status_code != 200:
                return build_response(503, JSON_TYPE, "Error occurred. Please login again.")
            else:
                orderAccessToken = reloginResponse.json.accessToken
                orderRefreshToken = reloginResponse.json.refreshToken
        else:
            orderAccessToken = refreshResponse.json.accessToken
            orderRefreshToken = refreshResponse.json.refreshToken

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        retrieveCartResponse = requests.get(f"{ORDER_URL}/cart", headers=headers)
        return build_response(retrieveCartResponse.status_code, JSON_TYPE, retrieveCartResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def clearShoppingCart(event):
    try:
        body = event.get('body') or '{}'
        orderAccessToken = extract_order_access_token(event)
        orderRefreshToken = extract_order_refresh_token(event)
        refreshBody = { "refreshToken": orderRefreshToken }
        refreshResponse = requests.post(f"{ORDER_URL}/auth/refresh", json=refreshBody)

        if refreshResponse.status_code != 200:
            email = (body.get("email") or "").strip().lower()
            password = body.get("password") or ""

            reloginBody = {
                "email": email,
                "password": password
            }
            reloginResponse = requests.post(f"{ORDER_URL}/auth/login", json=reloginBody)
            if reloginResponse.status_code != 200:
                return build_response(503, JSON_TYPE, "Error occurred. Please login again.")
            else:
                orderAccessToken = reloginResponse.json.accessToken
                orderRefreshToken = reloginResponse.json.refreshToken
        else:
            orderAccessToken = refreshResponse.json.accessToken
            orderRefreshToken = refreshResponse.json.refreshToken

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        clearCartResponse = requests.delete(f"{ORDER_URL}/cart", headers=headers)
        return build_response(clearCartResponse.status_code, JSON_TYPE, clearCartResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
