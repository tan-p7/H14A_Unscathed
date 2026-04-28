import requests
import json
from src.constants import ORDER_URL, UNSCATHED_EMAIL, UNSCATHED_PW
from src.shopping_cart import addItemToShoppingCart, removeItemFromShoppingCart, updateItemInShoppingCart, retrieveShoppingCart, clearShoppingCart
from src.order_api_handling import createOrder, retrieveOrderById, updateOrder, deleteOrder
import xml.etree.ElementTree as ET
import pytest

pytestmark = pytest.mark.skip(reason="Order API is non-functional")

NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'

# item_id = "f95f66f2-228c-4447-b3e1-32e501426b4e"

def parse_response_xml(body):
    if isinstance(body, str) and body.strip().startswith('"'):
        body = json.loads(body)
    return ET.fromstring(body.encode() if isinstance(body, str) else body)

def get_order_id(response):
    root = parse_response_xml(response)
    ids = root.findall(f'{{{NS_CBC}}}ID')
    return ids[0].text

class Test:

    def test_order(self):
        # make item
        loginBody = {
            "email": UNSCATHED_EMAIL,
            "password": UNSCATHED_PW
        }
        loginResponse = requests.post(f"{ORDER_URL}/auth/login", json=loginBody)
        assert loginResponse.status_code == 200

        orderAccessToken = loginResponse.json()['accessToken']

        authorization = "Bearer " + orderAccessToken
        headers = {
            "Authorization": authorization
        }

        item = {
            "itemName": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with 2.4GHz receiver",
            "price": 29.99,
            "quantityAvailable": 100,
            "imageUrl": "https://example.com/images/mouse.png"
        }
        makeItemResponse = requests.post(f"{ORDER_URL}/items", json=item, headers=headers)
        assert makeItemResponse.status_code == 201
        item_id = makeItemResponse.json()['item'][0]['item_id']

        # add to cart
        addToCartResponse = addItemToShoppingCart({ "itemId": item_id, "quantity": 2 })
        assert addToCartResponse["statusCode"] == 200

        # check cart
        retrieveCartResponse = retrieveShoppingCart()
        assert retrieveCartResponse["statusCode"] == 200

        # delete from cart
        deleteFromCartResponse = removeItemFromShoppingCart(item_id)
        assert deleteFromCartResponse["statusCode"] == 200

        # re add to cart
        addToCartResponse = addItemToShoppingCart({ "itemId": item_id, "quantity": 2 })
        assert addToCartResponse["statusCode"] == 200

        # order create
        createOrderResponse = createOrder()
        assert createOrderResponse["statusCode"] == 200

        order_id = get_order_id(createOrderResponse['body'])
        assert order_id is not None

        # order retrieve
        retrieveOrderResponse = retrieveOrderById(order_id)
        assert retrieveOrderResponse["statusCode"] == 200

        # order update
        update_body = {
            "userId": "d0bbc6a2-93db-42e3-a4c4-12133b5d625c",
            "updates": {
                "orderName": "Updated order",
                "accountingCost": 200
            }
        }
        updateOrderResponse = updateOrder(order_id, update_body)
        assert updateOrderResponse["statusCode"] == 200

        # order delete
        deleteOrderResponse = deleteOrder(order_id)
        assert deleteOrderResponse["statusCode"] == 200