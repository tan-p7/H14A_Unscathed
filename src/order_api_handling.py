# Import required modules for the API
from botocore.exceptions import ClientError
import requests
import json
from datetime import datetime

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE, ORDER_URL, UNSCATHED_SELLER_ID, UNSCATHED_EMAIL, UNSCATHED_PW

def createOrder():
    try:
        loginBody = {
            "email": UNSCATHED_EMAIL,
            "password": UNSCATHED_PW
        }
        loginResponse = requests.post(f"{ORDER_URL}/auth/login", json=loginBody)
        if loginResponse.status_code != 200:
            return build_response(503, JSON_TYPE, loginResponse.json())

        orderAccessToken = loginResponse.json()['accessToken']
        orderRefreshToken = loginResponse.json()['refreshToken']

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        retrieveCartResponse = requests.get(f"{ORDER_URL}/cart", headers=headers)
        if retrieveCartResponse.status_code != 200:
            return build_response(retrieveCartResponse.status_code, JSON_TYPE, retrieveCartResponse.json())

        cart = retrieveCartResponse.json()['items']
        order_items = []
        for item in cart:
            new_item = {
                "itemID": item['item_id'],
                "quantity": item['quantity'],
                "priceAtPurchase": float(item['price'])
            }
            order_items.append(new_item)

        now = datetime.now()
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

        logoutBody = {
            "refreshToken": orderRefreshToken
        }

        createOrderResponse = requests.post(f"{ORDER_URL}/orders", json=order_info, headers=headers)
        xml = createOrderResponse.text
        clearCartResponse = requests.delete(f"{ORDER_URL}/cart", headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(createOrderResponse.status_code, XML_TYPE, xml)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def retrieveOrderById(order_id):
    try:
        loginBody = {
            "email": UNSCATHED_EMAIL,
            "password": UNSCATHED_PW
        }
        loginResponse = requests.post(f"{ORDER_URL}/auth/login", json=loginBody)
        if loginResponse.status_code != 200:
            return build_response(503, JSON_TYPE, loginResponse.json())

        orderAccessToken = loginResponse.json()['accessToken']
        orderRefreshToken = loginResponse.json()['refreshToken']

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        logoutBody = {
            "refreshToken": orderRefreshToken
        }

        retrieveOrderResponse = requests.get(f"{ORDER_URL}/orders/{order_id}", headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(retrieveOrderResponse.status_code, JSON_TYPE, retrieveOrderResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def updateOrder(order_id, body):
    try:
        loginBody = {
            "email": UNSCATHED_EMAIL,
            "password": UNSCATHED_PW
        }
        loginResponse = requests.post(f"{ORDER_URL}/auth/login", json=loginBody)
        if loginResponse.status_code != 200:
            return build_response(503, JSON_TYPE, loginResponse.json())

        orderAccessToken = loginResponse.json()['accessToken']
        orderRefreshToken = loginResponse.json()['refreshToken']

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        update_body = body

        logoutBody = {
            "refreshToken": orderRefreshToken
        }

        updateOrderResponse = requests.put(f"{ORDER_URL}/orders/{order_id}", json=update_body, headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(updateOrderResponse.status_code, JSON_TYPE, updateOrderResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def deleteOrder(order_id):
    try:
        loginBody = {
            "email": UNSCATHED_EMAIL,
            "password": UNSCATHED_PW
        }
        loginResponse = requests.post(f"{ORDER_URL}/auth/login", json=loginBody)
        if loginResponse.status_code != 200:
            return build_response(503, JSON_TYPE, loginResponse.json())

        orderAccessToken = loginResponse.json()['accessToken']
        orderRefreshToken = loginResponse.json()['refreshToken']

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        logoutBody = {
            "refreshToken": orderRefreshToken
        }

        deleteOrderResponse = requests.delete(f"{ORDER_URL}/orders/{order_id}", headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(deleteOrderResponse.status_code, JSON_TYPE, deleteOrderResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
