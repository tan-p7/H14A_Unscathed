import json
import requests
import xml.etree.ElementTree as ET

BASE_URL = "https://y1j7xv2ua6.execute-api.us-east-1.amazonaws.com/v1/api/despatch"

NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'

VALID_ORDER_XML = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Order xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Order-2\"\n       xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\"\n       xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\">\n  <cbc:ID>ORD-001</cbc:ID>\n  <cbc:IssueDate>2025-03-01</cbc:IssueDate>\n  <cac:OrderReference>\n    <cbc:ID>ORD-001</cbc:ID>\n    <cbc:SalesOrderID>SALES-001</cbc:SalesOrderID>\n    <cbc:UUID>ABC-123-UUID</cbc:UUID>\n  </cac:OrderReference>\n  <cac:BuyerCustomerParty>\n    <cbc:CustomerAssignedAccountID>BUYER-ACC-1</cbc:CustomerAssignedAccountID>\n    <cbc:SupplierAssignedAccountID>SUP-ACC-1</cbc:SupplierAssignedAccountID>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Buyer Co</cbc:Name></cac:PartyName>\n      <cac:PostalAddress>\n        <cbc:StreetName>123 Buyer St</cbc:StreetName>\n        <cbc:CityName>Sydney</cbc:CityName>\n        <cbc:PostalZone>2000</cbc:PostalZone>\n        <cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country>\n      </cac:PostalAddress>\n    </cac:Party>\n  </cac:BuyerCustomerParty>\n  <cac:SellerSupplierParty>\n    <cbc:CustomerAssignedAccountID>SELLER-ACC-1</cbc:CustomerAssignedAccountID>\n    <cac:Party>\n      <cac:PartyName><cbc:Name>Seller Co</cbc:Name></cac:PartyName>\n    </cac:Party>\n  </cac:SellerSupplierParty>\n  <cac:Delivery>\n    <cac:DeliveryAddress>\n      <cbc:StreetName>456 Delivery Rd</cbc:StreetName>\n      <cbc:CityName>Melbourne</cbc:CityName>\n      <cbc:PostalZone>3000</cbc:PostalZone>\n      <cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country>\n    </cac:DeliveryAddress>\n  </cac:Delivery>\n  <cac:OrderLine>\n    <cac:LineItem>\n      <cbc:ID>1</cbc:ID>\n      <cbc:Quantity unitCode=\"EA\">5</cbc:Quantity>\n    </cac:LineItem>\n    <cac:Item>\n      <cbc:Description>Widget A</cbc:Description>\n      <cbc:Name>Widget</cbc:Name>\n      <cac:BuyersItemIdentification><cbc:ID>B-ITEM-1</cbc:ID></cac:BuyersItemIdentification>\n      <cac:SellersItemIdentification><cbc:ID>S-ITEM-1</cbc:ID></cac:SellersItemIdentification>\n    </cac:Item>\n  </cac:OrderLine>\n</Order>"


def parse_response_xml(body):
    if isinstance(body, str) and body.strip().startswith('"'):
        body = json.loads(body)
    return ET.fromstring(body.encode() if isinstance(body, str) else body)


def get_despatch_id(response):
    root = parse_response_xml(response)
    ids = root.findall(f'{{{NS_CBC}}}ID')
    return ids[0].text


class TestHealthCheck:

    def test_health_check_returns_200(self):
        response = requests.get(f"{BASE_URL}/health")

        assert response.status_code == 200

class TestGenerateDespatch:

    def test_successfully_generates_despatch(self):

        response = requests.post(
            f"{BASE_URL}/despatch-advice",
            json=VALID_ORDER_XML
        )

        assert response.status_code == 200

        root = parse_response_xml(response.text)
        assert root is not None

        despatch_id = get_despatch_id(response.text)

        assert despatch_id is not None
        assert len(despatch_id) == 9
        assert despatch_id.isdigit()

    def test_fails_with_empty_body(self):

        response = requests.post(
            f"{BASE_URL}/despatch-advice",
            json=""
        )

        assert response.status_code == 400

class TestRetrieveAllDespatch:

    def test_successfully_retrieves_all_despatches(self):

        response = requests.get(f"{BASE_URL}/despatch-advice")
        assert response.status_code == 200

        root = parse_response_xml(response.text)
        assert root is not None

class TestRetrieveDespatch:

    def test_successfully_retrieves_despatch(self):

        create_response = requests.post(
            f"{BASE_URL}/despatch-advice",
            json=VALID_ORDER_XML
        )

        assert create_response.status_code == 200

        despatch_id = get_despatch_id(create_response.text)

        response = requests.get(
            f"{BASE_URL}/despatch-advice/{despatch_id}"
        )

        assert response.status_code == 200
        assert response.headers["Content-Type"].startswith("application/xml")

        returned_id = get_despatch_id(response.text)
        assert returned_id == despatch_id
    
    def test_fails_to_retrieve_nonexistent_despatch(self):

        response = requests.get(
            f"{BASE_URL}/despatch-advice/nonexistent"
        )

        assert response.status_code == 404

class TestUpdateDespatch:

    def test_successfully_updates_delivered_quantity(self):

        create_response = requests.post(
            f"{BASE_URL}/despatch-advice",
            json=VALID_ORDER_XML
        )

        assert create_response.status_code == 200

        despatch_id = get_despatch_id(create_response.text)

        body = {"deliveredQuantity": 10}

        response = requests.put(
            f"{BASE_URL}/despatch-advice/{despatch_id}",
            json=body
        )

        assert response.status_code == 200

        root = parse_response_xml(response.text)
        dq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}DeliveredQuantity")
        assert dq is not None
        assert dq.text == "10"

    def test_fails_to_update_nonexistent_despatch(self):

        body = {"deliveredQuantity": 10}

        response = requests.put(
            f"{BASE_URL}/despatch-advice/nonexistent",
            json=body
        )

        assert response.status_code == 404

class TestDeleteDespatch:

    def test_successfully_deletes_despatch(self):

        create_response = requests.post(
            f"{BASE_URL}/despatch-advice",
            json=VALID_ORDER_XML
        )

        assert create_response.status_code == 200

        despatch_id = get_despatch_id(create_response.text)
        delete_response = requests.delete(
            f"{BASE_URL}/despatch-advice/{despatch_id}"
        )

        assert delete_response.status_code == 204

        retrieve_response = requests.get(
            f"{BASE_URL}/despatch-advice/{despatch_id}"
        )

        assert retrieve_response.status_code == 404


    def test_fails_to_delete_nonexistent_despatch(self):

        response = requests.delete(
            f"{BASE_URL}/despatch-advice/nonexistent"
        )

        assert response.status_code == 404

