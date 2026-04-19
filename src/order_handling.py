# Import required modules for the API
from botocore.exceptions import ClientError
import requests
from datetime import datetime

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE, ORDER_URL, UNSCATHED_SELLER_ID
from src.auth_dependencies import extract_order_access_token, extract_order_refresh_token

def createOrder(event):
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
        if retrieveCartResponse.status_code != 200:
            return build_response(retrieveCartResponse.status_code, JSON_TYPE, retrieveCartResponse.json)

        cart = retrieveCartResponse.json.items
        order_items = []
        for item in cart:
            new_item = {
                "itemID": item.item_id,
                "quantity": item.quantity,
                "priceAtPurchase": item.price
            }
            order_items.append(new_item)

        order_time = now.strftime("%Y-%m-%d %H:%M:%S")

        order_info = {
            "orderName": "Purchase Order " + order_time,
            "sellerId": UNSCATHED_SELLER_ID,
            "documentCurrencyCode": "AUD",
            "pricingCurrencyCode": "AUD",
            "taxCurrencyCode": "AUD",
            "requestedInvoiceCurrencyCode": "AUD",
            "accountingCost": 150,
            "paymentMethodCode": "CreditCard",
            "destinationCountryCode": "AU",
            "orderLines": order_items
        }

        createOrderResponse = requests.post(f"{ORDER_URL}/orders", json=order_info, headers=headers)
        return build_response(createOrderResponse.status_code, JSON_TYPE, createOrderResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def retrieveOrderById(event):
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

        order_id = event['pathParameters'].get('order-id')

        retrieveOrderResponse = requests.get(f"{ORDER_URL}/orders/{order_id}", headers=headers)
        return build_response(retrieveOrderResponse.status_code, JSON_TYPE, retrieveOrderResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def updateOrder(event):
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

        order_id = event['pathParameters'].get('order-id')
        order_time = now.strftime("%Y-%m-%d %H:%M:%S")
        update_body = {
            "userId": body.get("user-id", ""),
            "updates": {
                "orderName": body.get("order-name", order_time),
                "accountingCost": body.get("accounting-cost", 150)
            }
        }

        updateOrderResponse = requests.put(f"{ORDER_URL}/orders/{order_id}", headers=headers)
        return build_response(updateOrderResponse.status_code, JSON_TYPE, updateOrderResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def deleteOrder(event):
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

        order_id = event['pathParameters'].get('order-id')
        deleteOrderResponse = requests.delete(f"{ORDER_URL}/orders/{order_id}", headers=headers)
        return build_response(deleteOrderResponse.status_code, JSON_TYPE, deleteOrderResponse.json)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
