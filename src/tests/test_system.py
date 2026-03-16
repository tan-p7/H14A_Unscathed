import json
import xml.etree.ElementTree as ET
from src.generate_despatch import generate_despatch
from src.db import dynamodb_table
from src.lambda_function import lambda_handler

NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'

VALID_ORDER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Order xmlns="urn:oasis:names:specification:ubl:schema:xsd:Order-2"
       xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
       xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2">
  <cbc:ID>ORD-001</cbc:ID>
  <cbc:IssueDate>2025-03-01</cbc:IssueDate>
  <cac:OrderReference>
    <cbc:ID>ORD-001</cbc:ID>
    <cbc:SalesOrderID>SALES-001</cbc:SalesOrderID>
    <cbc:UUID>ABC-123-UUID</cbc:UUID>
  </cac:OrderReference>
  <cac:BuyerCustomerParty>
    <cbc:CustomerAssignedAccountID>BUYER-ACC-1</cbc:CustomerAssignedAccountID>
    <cbc:SupplierAssignedAccountID>SUP-ACC-1</cbc:SupplierAssignedAccountID>
    <cac:Party>
      <cac:PartyName><cbc:Name>Buyer Co</cbc:Name></cac:PartyName>
      <cac:PostalAddress>
        <cbc:StreetName>123 Buyer St</cbc:StreetName>
        <cbc:CityName>Sydney</cbc:CityName>
        <cbc:PostalZone>2000</cbc:PostalZone>
        <cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country>
      </cac:PostalAddress>
    </cac:Party>
  </cac:BuyerCustomerParty>
  <cac:SellerSupplierParty>
    <cbc:CustomerAssignedAccountID>SELLER-ACC-1</cbc:CustomerAssignedAccountID>
    <cac:Party>
      <cac:PartyName><cbc:Name>Seller Co</cbc:Name></cac:PartyName>
    </cac:Party>
  </cac:SellerSupplierParty>
  <cac:Delivery>
    <cac:DeliveryAddress>
      <cbc:StreetName>456 Delivery Rd</cbc:StreetName>
      <cbc:CityName>Melbourne</cbc:CityName>
      <cbc:PostalZone>3000</cbc:PostalZone>
      <cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country>
    </cac:DeliveryAddress>
  </cac:Delivery>
  <cac:OrderLine>
    <cac:LineItem>
      <cbc:ID>1</cbc:ID>
      <cbc:Quantity unitCode="EA">5</cbc:Quantity>
    </cac:LineItem>
    <cac:Item>
      <cbc:Description>Widget A</cbc:Description>
      <cbc:Name>Widget</cbc:Name>
      <cac:BuyersItemIdentification><cbc:ID>B-ITEM-1</cbc:ID></cac:BuyersItemIdentification>
      <cac:SellersItemIdentification><cbc:ID>S-ITEM-1</cbc:ID></cac:SellersItemIdentification>
    </cac:Item>
  </cac:OrderLine>
</Order>"""



def make_lambda_event(method, path, body=None, path_parameters=None):
    return {
        "httpMethod": method,
        "path": path,
        "pathParameters": path_parameters,
        "body": body
    }

def parse_response_xml(response):
    body = response['body']
    if isinstance(body, str) and body.strip().startswith('"'):
        body = json.loads(body)
    return ET.fromstring(body.encode() if isinstance(body, str) else body)


def get_despatch_id_from_response(response):
    root = parse_response_xml(response)
    ids = root.findall(f'{{{NS_CBC}}}ID')
    return ids[0].text




class TestHealthCheck:
    def test_health_check_returns_200(self):
        event = make_lambda_event("GET", "/api/despatch/health")
        response = lambda_handler(event, {})
        assert response["statusCode"] == 200


class TestGenerateDespatch:
    def test_successfully_generates_despatch(self):
        event = make_lambda_event(
            "POST",
            "/api/despatch/despatch-advice",
            body=VALID_ORDER_XML
        )
        response = lambda_handler(event, {})

        assert response["statusCode"] == 200

        root = parse_response_xml(response)
        assert root is not None

        despatch_id = get_despatch_id_from_response(response)
        assert despatch_id is not None
        assert len(despatch_id) == 9
        assert despatch_id.isdigit()

    def test_fails_with_invalid_xml(self):
        event = make_lambda_event(
            "POST",
            "/api/despatch/despatch-advice",
            body="this is not xml"
        )
        response = lambda_handler(event, {})
        assert response["statusCode"] == 400

    def test_fails_with_empty_body(self):
        event = make_lambda_event(
            "POST",
            "/api/despatch/despatch-advice",
            body=None
        )
        response = lambda_handler(event, {})
        assert response["statusCode"] == 400


class TestRetrieveAllDespatch:
    def test_successfully_retrieves_all_despatches(self):
        event = make_lambda_event("GET", "/api/despatch/despatch-advice")
        response = lambda_handler(event, {})
        assert response["statusCode"] == 200


class TestRetrieveDespatch:
    def test_successfully_retrieves_despatch(self):
        create_response = lambda_handler(make_lambda_event(
            "POST",
            "/api/despatch/despatch-advice",
            body=VALID_ORDER_XML
        ), {})
        assert create_response["statusCode"] == 200
        despatch_id = get_despatch_id_from_response(create_response)

        response = lambda_handler(make_lambda_event(
            "GET",
            f"/api/despatch/despatch-advice/{despatch_id}",
            path_parameters={"despatch-id": despatch_id}
        ), {})

        assert response["statusCode"] == 200
        assert response["headers"]["Content-Type"] == "application/xml"

        root = parse_response_xml(response)
        returned_id = root.findall(f'{{{NS_CBC}}}ID')[0].text
        assert returned_id == despatch_id

    def test_returns_404_for_nonexistent_despatch(self):
        response = lambda_handler(make_lambda_event(
            "GET",
            "/api/despatch/despatch-advice/nonexistent-999",
            path_parameters={"despatch-id": "nonexistent-999"}
        ), {})
        assert response["statusCode"] == 404


class TestDeleteDespatch:
    def test_successfully_deletes_despatch(self):
        create_response = lambda_handler(make_lambda_event(
            "POST",
            "/api/despatch/despatch-advice",
            body=VALID_ORDER_XML
        ), {})
        assert create_response["statusCode"] == 200
        despatch_id = get_despatch_id_from_response(create_response)

        delete_response = lambda_handler(make_lambda_event(
            "DELETE",
            f"/api/despatch/despatch-advice/{despatch_id}",
            path_parameters={"despatch-id": despatch_id}
        ), {})
        assert delete_response["statusCode"] == 204

        retrieve_response = lambda_handler(make_lambda_event(
            "GET",
            f"/api/despatch/despatch-advice/{despatch_id}",
            path_parameters={"despatch-id": despatch_id}
        ), {})
        assert retrieve_response["statusCode"] == 404

    def test_fails_to_delete_nonexistent_despatch(self):
        response = lambda_handler(make_lambda_event(
            "DELETE",
            "/api/despatch/despatch-advice/nonexistent-999",
            path_parameters={"despatch-id": "nonexistent-999"}
        ), {})
        assert response["statusCode"] == 404


