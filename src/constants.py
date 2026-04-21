import requests

JSON_TYPE = 'application/json'
XML_TYPE = 'application/xml'








response = requests.post("https://lastminutepush.one/auth/register", json ={
    "groupName": "unscathed"

}) 

INVOICE_URL = "https://lastminutepush.one/"
INVOICE_API_KEY = response.json()['apiKey']
