import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock
from generate_despatch import generate_despatch

# ── Namespaces ──────────────────────────────────────────────────────────────
NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'

# ── Helpers ─────────────────────────────────────────────────────────────────

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


def make_event(xml_string):
    """Helper to wrap XML in the event dict the function expects."""
    return {'body': xml_string}


def parse_response_xml(response):
    """Helper to parse the returned despatch XML string."""
    return ET.fromstring(response['body'].encode())


# ── Tests: valid despatch advice ─────────────────────────────────────────────

class TestValidDespatch:

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_returns_200(self, mock_schema):
        mock_schema.return_value.validate.return_value = None  # skip real schema
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        assert response['statusCode'] == 200

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_returns_xml_content_type(self, mock_schema):
        mock_schema.return_value.validate.return_value = None
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        assert response['headers']['Content-Type'] == 'application/xml'

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_body_is_valid_xml(self, mock_schema):
        mock_schema.return_value.validate.return_value = None
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        # should not raise
        root = parse_response_xml(response)
        assert root is not None

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_order_reference_id_matches(self, mock_schema):
        mock_schema.return_value.validate.return_value = None
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        root = parse_response_xml(response)
        order_ref_id = root.findtext(
            f'.//{{{NS_CAC}}}OrderReference/{{{NS_CBC}}}ID'
        )
        assert order_ref_id == 'ORD-001'

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_despatch_line_quantity(self, mock_schema):
        mock_schema.return_value.validate.return_value = None
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        root = parse_response_xml(response)
        qty = root.findtext(f'.//{{{NS_CBC}}}DeliveredQuantity')
        assert qty == '5'

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_delivery_address_populated(self, mock_schema):
        mock_schema.return_value.validate.return_value = None
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        root = parse_response_xml(response)
        city = root.findtext(
            f'.//{{{NS_CAC}}}DeliveryAddress/{{{NS_CBC}}}CityName'
        )
        assert city == 'Melbourne'

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_delivery_dates_auto_generated(self, mock_schema):
        mock_schema.return_value.validate.return_value = None
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        root = parse_response_xml(response)
        start = root.findtext(f'.//{{{NS_CBC}}}StartDate')
        end = root.findtext(f'.//{{{NS_CBC}}}EndDate')
        assert start is not None
        assert end is not None
        assert end > start  # end date is after start date

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_multiple_order_lines(self, mock_schema):
        mock_schema.return_value.validate.return_value = None
        multi_line_xml = VALID_ORDER_XML.replace(
            '</Order>',
            """<cac:OrderLine>
                <cac:LineItem><cbc:ID>2</cbc:ID><cbc:Quantity unitCode="EA">3</cbc:Quantity></cac:LineItem>
                <cac:Item><cbc:Name>Widget B</cbc:Name></cac:Item>
               </cac:OrderLine></Order>"""
        )
        response = generate_despatch(make_event(multi_line_xml), {})
        root = parse_response_xml(response)
        lines = root.findall(
            f'.//{{{NS_CAC}}}DespatchLine'
        )
        assert len(lines) == 2


# ── Tests: error cases ───────────────────────────────────────────────────────

class TestErrorCases:

    def test_invalid_xml_returns_400(self):
        response = generate_despatch(make_event("this is not xml at all"), {})
        assert response['statusCode'] == 400

    def test_empty_body_returns_400(self):
        response = generate_despatch(make_event(""), {})
        assert response['statusCode'] == 400

    @patch('generate_despatch.xmlschema.XMLSchema')
    def test_schema_validation_failure_returns_400(self, mock_schema):
        import xmlschema
        mock_schema.return_value.validate.side_effect = (
            xmlschema.XMLSchemaValidationError(mock_schema, "bad xml")
        )
        response = generate_despatch(make_event(VALID_ORDER_XML), {})
        assert response['statusCode'] == 400
        assert 'Invalid Order XML' in response['body']

    def test_missing_body_key_returns_400(self):
        response = generate_despatch({}, {})  # no 'body' key
        assert response['statusCode'] == 400