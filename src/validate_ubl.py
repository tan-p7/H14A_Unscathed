# Import required modules for the API
from botocore.exceptions import ClientError
import requests
import json

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE, DEVEX_API_KEY, DEVEX_VALIDATION_URL, BROWN_BANDITS_VALIDATION_URL

def validate_order(xml):
    try:
        headers = {
            "Api-Key": DEVEX_API_KEY,
            "Content-Type": XML_TYPE
        }
        validateResponse = requests.post(f"{DEVEX_VALIDATION_URL}/order", json=xml, headers=headers)
        parsedResponse = validateResponse.json()

        valid = False
        if len(parsedResponse['errors']) == 0:
            valid = True

        return_object = {
            "valid": valid,
            "errors": parsedResponse['errors']
        }
        return build_response(validateResponse.status_code, JSON_TYPE, return_object)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def validate_despatch(xml):
    try:
        headers = {
            "Api-Key": DEVEX_API_KEY,
            "Content-Type": XML_TYPE
        }
        validateResponse = requests.post(f"{DEVEX_VALIDATION_URL}/despatch", json=xml, headers=headers)
        parsedResponse = validateResponse.json()

        valid = False
        if len(parsedResponse['errors']) == 0:
            valid = True

        return_object = {
            "valid": valid,
            "errors": parsedResponse['errors']
        }
        return build_response(validateResponse.status_code, JSON_TYPE, return_object)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])

def validate_invoice(xml):
    try:
        payload = {
            "invoice_xml": xml,
            "ruleset": "ubl"
        }
        validateResponse = requests.post(f"{BROWN_BANDITS_VALIDATION_URL}", json=payload)
        parsedResponse = validateResponse.json()

        valid = False
        if len(parsedResponse['errors']) == 0:
            valid = True

        return_object = {
            "valid": valid,
            "errors": parsedResponse['errors']
        }
        return build_response(validateResponse.status_code, JSON_TYPE, return_object)

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
