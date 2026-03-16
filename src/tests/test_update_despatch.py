# Import python modules needed for testing
import json
import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from botocore.exceptions import ClientError

# Import function to test
from src.update_despatch import update_despatch_advice, _is_numeric

# Minimal valid despatch XML with one DespatchLine (namespaces match update_despatch)
NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
NS_UBL = 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2'

VALID_DESPATCH_XML = f"""<?xml version="1.0"?>
<DespatchAdvice xmlns="{NS_UBL}" xmlns:cbc="{NS_CBC}" xmlns:cac="{NS_CAC}">
  <cbc:ID>123</cbc:ID>
  <cac:DespatchLine>
    <cbc:DeliveredQuantity unitCode="EA">1</cbc:DeliveredQuantity>
  </cac:DespatchLine>
</DespatchAdvice>"""


class TestIsNumeric:
    """Tests for _is_numeric helper (int and float accepted, bool rejected)."""

    def test_accepts_int(self):
        assert _is_numeric(0) is True
        assert _is_numeric(5) is True
        assert _is_numeric(-1) is True

    def test_accepts_float(self):
        assert _is_numeric(0.0) is True
        assert _is_numeric(5.0) is True
        assert _is_numeric(3.14) is True

    def test_rejects_bool(self):
        assert _is_numeric(True) is False
        assert _is_numeric(False) is False

    def test_rejects_non_numeric(self):
        assert _is_numeric("5") is False
        assert _is_numeric(None) is False
        assert _is_numeric([1]) is False


class TestUpdateDespatchAdviceSuccess:
    """Tests for successful update paths."""

    def test_successfully_updates_with_int_quantities(self):
        body = json.dumps({"deliveredQuantity": 10, "backorderQuantity": 2})
        mock_get = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = mock_get
            mock_table.update_item.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            assert response["headers"]["Content-Type"] == "application/xml"
            mock_table.get_item.assert_called_once_with(Key={"despatch_id": "123"})
            mock_table.update_item.assert_called_once()
            call_kw = mock_table.update_item.call_args[1]
            assert call_kw["Key"] == {"despatch_id": "123"}
            updated = call_kw["ExpressionAttributeValues"][":xml"]
            root = ET.fromstring(updated)
            dq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}DeliveredQuantity")
            assert dq is not None and dq.text == "10"
            bq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}BackorderQuantity")
            assert bq is not None and bq.text == "2"

    def test_successfully_updates_with_float_quantities(self):
        """Accept float deliveredQuantity and backorderQuantity (e.g. 5.0 from JSON)."""
        body = json.dumps({"deliveredQuantity": 5.0, "backorderQuantity": 2.0})
        mock_get = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = mock_get
            mock_table.update_item.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            mock_table.update_item.assert_called_once()
            call_kw = mock_table.update_item.call_args[1]
            updated = call_kw["ExpressionAttributeValues"][":xml"]
            root = ET.fromstring(updated)
            dq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}DeliveredQuantity")
            assert dq is not None and dq.text == "5.0"
            bq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}BackorderQuantity")
            assert bq is not None and bq.text == "2.0"

    def test_successfully_updates_note_only(self):
        body = json.dumps({"note": "Delivered late"})
        mock_get = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = mock_get
            mock_table.update_item.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            call_kw = mock_table.update_item.call_args[1]
            updated = call_kw["ExpressionAttributeValues"][":xml"]
            root = ET.fromstring(updated)
            note_el = root.find(f"{{{NS_CBC}}}Note")
            assert note_el is not None and note_el.text == "Delivered late"

    def test_successfully_updates_backorder_reason(self):
        body = json.dumps({"backorderQuantity": 1, "backorderReason": "Out of stock"})
        mock_get = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = mock_get
            mock_table.update_item.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            call_kw = mock_table.update_item.call_args[1]
            updated = call_kw["ExpressionAttributeValues"][":xml"]
            root = ET.fromstring(updated)
            br = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}BackorderReason")
            assert br is not None and br.text == "Out of stock"


class TestUpdateDespatchAdviceValidation:
    """Tests for request validation (400)."""

    def test_invalid_json_returns_400(self):
        response = update_despatch_advice("123", "not json at all")
        assert response["statusCode"] == 400
        assert "Invalid JSON" in json.loads(response["body"])

    def test_delivered_quantity_must_be_number_string_rejected(self):
        body = json.dumps({"deliveredQuantity": "ten"})
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}
            response = update_despatch_advice("123", body)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Delivered quantity must be a number."

    def test_delivered_quantity_bool_rejected(self):
        body = json.dumps({"deliveredQuantity": True})
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}
            response = update_despatch_advice("123", body)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Delivered quantity must be a number."

    def test_backorder_quantity_must_be_number(self):
        body = json.dumps({"backorderQuantity": "two"})
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}
            response = update_despatch_advice("123", body)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Backorder quantity must be a number."

    def test_backorder_reason_must_be_text(self):
        body = json.dumps({"backorderReason": 123})
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}
            response = update_despatch_advice("123", body)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Backorder reason must be text."

    def test_note_must_be_text(self):
        body = json.dumps({"note": 999})
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}
            response = update_despatch_advice("123", body)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == "Note must be text."


class TestUpdateDespatchAdviceNotFoundAndErrors:
    """Tests for 404, 500, 503."""

    def test_returns_404_when_despatch_not_found(self):
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {}
            response = update_despatch_advice("999", "{}")
        assert response["statusCode"] == 404
        assert "999" in json.loads(response["body"])
        mock_table.update_item.assert_not_called()

    def test_returns_500_when_stored_xml_invalid(self):
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {"Item": {"despatch_ubl": "<not valid xml"}}
            response = update_despatch_advice("123", "{}")
        assert response["statusCode"] == 500
        assert "invalid xml" in json.loads(response["body"]).lower()
        mock_table.update_item.assert_not_called()

    def test_returns_503_on_client_error_get_item(self):
        error = ClientError(
            {"Error": {"Code": "InternalServerError", "Message": "DynamoDB failure"}},
            "GetItem",
        )
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.side_effect = error
            response = update_despatch_advice("123", "{}")
        assert response["statusCode"] == 503
        assert "DynamoDB" in json.loads(response["body"]) or "failure" in json.loads(response["body"]).lower()

    def test_returns_503_on_client_error_update_item(self):
        error = ClientError(
            {"Error": {"Code": "InternalServerError", "Message": "Update failed"}},
            "UpdateItem",
        )
        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table:
            mock_table.get_item.return_value = {"Item": {"despatch_ubl": VALID_DESPATCH_XML}}
            mock_table.update_item.side_effect = error
            response = update_despatch_advice("123", "{}")
        assert response["statusCode"] == 503
