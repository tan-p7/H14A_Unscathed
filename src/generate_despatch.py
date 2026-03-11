import json
import xml.etree.ElementTree as ET
from datetime import date



def handler(event, context):

    try:
        body = json.loads(event["body"])

        order_xml = body["orderXml"]
        delivered = body["deliveredQuantity"]
        backorder = body["backorderQuantity"]
        reason = body["backorderReason"]
        note = body.get("note", "")

        root = ET.fromstring(order_xml)

        NS = {
            "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
        }

        order_reference = root.find(".//cac:OrderReference/cbc:ID", NS).text
        seller_name = root.find(".//cac:SellerSupplierParty//cbc:Name", NS).text
        buyer_name = root.find(".//cac:BuyerCustomerParty//cbc:Name", NS).text

        line_ids = [
            line.text
            for line in root.findall(".//cac:OrderLine/cac:LineItem/cbc:ID", NS)
        ]

        despatch_root = ET.Element(
            "DespatchAdvice",
            {
                "xmlns": "urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2",
                "xmlns:cbc": NS["cbc"],
                "xmlns:cac": NS["cac"]
            }
        )

        ET.SubElement(despatch_root, "cbc:UBLVersionID").text = "2.1"
      

        # Despatch lines
        for line_id in line_ids:
            line = ET.SubElement(despatch_root, "cac:DespatchLine")

            ET.SubElement(line, "cbc:ID").text = line_id

            delivered_q = ET.SubElement(
                line,
                "cbc:DeliveredQuantity",
                {"unitCode": "KGM"}
            )
            delivered_q.text = str(delivered)

            backorder_q = ET.SubElement(
                line,
                "cbc:BackorderQuantity",
                {"unitCode": "KGM"}
            )
            backorder_q.text = str(backorder)

            ET.SubElement(line, "cbc:BackorderReason").text = reason

        despatch_xml = ET.tostring(despatch_root, encoding="unicode")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/xml"
            },
            "body": despatch_xml
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }