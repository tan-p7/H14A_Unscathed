# Import required modules for the API
from botocore.exceptions import ClientError
import requests
import json

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, ORDER_URL, UNSCATHED_EMAIL, UNSCATHED_PW

def addItemToShoppingCart(body):
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
    
        addToCartResponse = requests.post(f"{ORDER_URL}/cart/items", json=body, headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)

        return build_response(addToCartResponse.status_code, JSON_TYPE, addToCartResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def removeItemFromShoppingCart(itemId):
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

        removeFromCartResponse = requests.delete(f"{ORDER_URL}/cart/items/{itemId}", headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(removeFromCartResponse.status_code, JSON_TYPE, removeFromCartResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def updateItemInShoppingCart(itemId, quantity):
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

        updateCartResponse = requests.put(f"{ORDER_URL}/cart/items/{itemId}", json={ "quantity": quantity }, headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(updateCartResponse.status_code, JSON_TYPE, updateCartResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def retrieveShoppingCart():
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

        retrieveCartResponse = requests.get(f"{ORDER_URL}/cart", headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(retrieveCartResponse.status_code, JSON_TYPE, retrieveCartResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def clearShoppingCart():
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

        clearCartResponse = requests.delete(f"{ORDER_URL}/cart", headers=headers)
        logoutResponse = requests.post(f"{ORDER_URL}/auth/logout", json=logoutBody, headers=headers)
        return build_response(clearCartResponse.status_code, JSON_TYPE, clearCartResponse.json())

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
