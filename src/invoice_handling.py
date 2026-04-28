# Import required modules for the API
from botocore.exceptions import ClientError
import requests
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE, INVOICE_URL, INVOICE_API_KEY

HEADERS = {"X-API-Key": INVOICE_API_KEY}

def createInvoice():
    try:
        invoice_info = {
            "order_reference":"ORD-1001",
            "customer_id": "CUST-2001",
            "issue_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": "2026-07-23",
            "currency": "AUD",
            "supplier": {
                "name": "Invoice Generation API Supplier",
                "identifier": "OUR-COMPANY"
            },
            "customer": {
                "name": "Customer A",
                "identifier": "CUST-2001"
            },
            "items": [
                {
                "name": "Consulting Service",
                "description": "Business consulting engagement",
                "quantity": 1,
                "unit_price": 99.99,
                "unit_code": "EA"
                }
            ]
        }
    
        response = requests.post(f"{INVOICE_URL}/v1/invoices", json=invoice_info, headers=HEADERS)
        return build_response(response.status_code, JSON_TYPE, response.json())
    except ClientError as e:
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])


def retrieveInvoiceById(invoice_id):
    try:
        response = requests.get(f"{INVOICE_URL}/v1/invoices/{invoice_id}", headers=HEADERS)
        return build_response(response.status_code, JSON_TYPE, response.json())
    except ClientError as e:
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
    

def updateInvoiceById(invoice_id):
    try:
        update_info = {
            "order_reference": "ORD-UPDATED",
            "issue_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": "2026-07-28",
            "currency": "AUD",
            "supplier": {
                "name": "Updated Supplier",
                "identifier": "SUP-001"
            },
            "customer": {
                "name": "Updated Customer",
                "identifier": "CUST-2001"
            },
            "items": [
                {
                    "name": "Updated Service",
                    "description": "Repriced work",
                    "quantity": 2,
                    "unit_price": 12.5,
                    "unit_code": "EA"
                }
            ]
        }   
        response = requests.put(f"{INVOICE_URL}/v1/invoices/{invoice_id}", json=update_info, headers=HEADERS)
        return build_response(response.status_code, JSON_TYPE, response.json())
    except ClientError as e:
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])


def deleteInvoiceById(invoice_id):
    try:
        response = requests.delete(f"{INVOICE_URL}/v1/invoices/{invoice_id}", headers=HEADERS)
        if response.status_code == 204:
            return build_response(204, JSON_TYPE, {"message": "Invoice deleted successfully"})
        return build_response(response.status_code, JSON_TYPE, response.json())
    except ClientError as e:
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])
    
def InvoiceStatus(invoice_id):
    try:
        status_info = {
            "status": "sent"
        }
        response = requests.post(f"{INVOICE_URL}/v1/invoices/{invoice_id}/status", json=status_info, headers=HEADERS)
        return build_response(response.status_code, JSON_TYPE, response.json())
    except ClientError as e:
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])



def createCreditNote(invoice_id):
    try:
        credit_note_info = {
            "reason": "Customer order cancelled after invoicing"
        }
        response = requests.post(f"{INVOICE_URL}/v1/invoices/{invoice_id}/credit-note", json=credit_note_info, headers=HEADERS)
        return build_response(response.status_code, JSON_TYPE, response.json())
    except ClientError as e:
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])


def InvoiceToPdf(invoice_id):
    try:
        response = requests.get(f"{INVOICE_URL}/v1/invoices/{invoice_id}/pdf", headers=HEADERS)
        return {"statusCode": response.status_code, "body": response.content}
    except ClientError as e:
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])






