# Import python modules needed for testing
import json
import io
import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock
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
        mock_get = {"Item": {"despatch_id": "123"}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table, \
             patch("src.update_despatch.s3.s3_client") as mock_s3_client, \
             patch("src.update_despatch.s3.BUCKET_NAME", "mock-bucket"):

            mock_table.get_item.return_value = mock_get
            mock_s3_client.get_object.return_value = {
                'Body': io.BytesIO(VALID_DESPATCH_XML.encode('utf-8'))
            }
            mock_s3_client.put_object.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            mock_s3_client.put_object.assert_called_once()
            updated_xml = mock_s3_client.put_object.call_args[1]['Body'].decode('utf-8')
            root = ET.fromstring(updated_xml)

            dq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}DeliveredQuantity")
            assert dq is not None and dq.text == "10"

            bq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}BackorderQuantity")
            assert bq is not None and bq.text == "2"

    def test_successfully_updates_with_float_quantities(self):
        body = json.dumps({"deliveredQuantity": 5.0, "backorderQuantity": 2.0})
        mock_get = {"Item": {"despatch_id": "123"}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table, \
             patch("src.update_despatch.s3.s3_client") as mock_s3_client, \
             patch("src.update_despatch.s3.BUCKET_NAME", "mock-bucket"):

            mock_table.get_item.return_value = mock_get
            mock_s3_client.get_object.return_value = {
                'Body': io.BytesIO(VALID_DESPATCH_XML.encode('utf-8'))
            }
            mock_s3_client.put_object.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            mock_s3_client.put_object.assert_called_once()
            updated_xml = mock_s3_client.put_object.call_args[1]['Body'].decode('utf-8')
            root = ET.fromstring(updated_xml)

            dq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}DeliveredQuantity")
            assert dq is not None and dq.text == "5.0"

            bq = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}BackorderQuantity")
            assert bq is not None and bq.text == "2.0"

    def test_successfully_updates_note_only(self):
        body = json.dumps({"note": "Delivered late"})
        mock_get = {"Item": {"despatch_id": "123"}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table, \
             patch("src.update_despatch.s3.s3_client") as mock_s3_client, \
             patch("src.update_despatch.s3.BUCKET_NAME", "mock-bucket"):

            mock_table.get_item.return_value = mock_get
            mock_s3_client.get_object.return_value = {
                'Body': io.BytesIO(VALID_DESPATCH_XML.encode('utf-8'))
            }
            mock_s3_client.put_object.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            updated_xml = mock_s3_client.put_object.call_args[1]['Body'].decode('utf-8')
            root = ET.fromstring(updated_xml)

            note_el = root.find(f"{{{NS_CBC}}}Note")
            assert note_el is not None and note_el.text == "Delivered late"

    def test_successfully_updates_backorder_reason(self):
        body = json.dumps({"backorderQuantity": 1, "backorderReason": "Out of stock"})
        mock_get = {"Item": {"despatch_id": "123"}}

        with patch("src.update_despatch.src.db.dynamodb_table") as mock_table, \
             patch("src.update_despatch.s3.s3_client") as mock_s3_client, \
             patch("src.update_despatch.s3.BUCKET_NAME", "mock-bucket"):

            mock_table.get_item.return_value = mock_get
            mock_s3_client.get_object.return_value = {
                'Body': io.BytesIO(VALID_DESPATCH_XML.encode('utf-8'))
            }
            mock_s3_client.put_object.return_value = {}

            response = update_despatch_advice("123", body)

            assert response["statusCode"] == 200
            updated_xml = mock_s3_client.put_object.call_args[1]['Body'].decode('utf-8')
            root = ET.fromstring(updated_xml)

            br = root.find(f".//{{{NS_CAC}}}DespatchLine/{{{NS_CBC}}}BackorderReason")
            assert br is not None and br.text == "Out of stock"