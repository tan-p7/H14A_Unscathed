# Import required modules for the API
import json
import xml.etree.ElementTree as ET
from botocore.exceptions import ClientError
from json import JSONDecodeError

# Import helper function and constants to build the JSON response
from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE
import src.db
import src.s3 as s3

NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'


def _is_numeric(value):
    """Return True if value is int or float but not bool (since bool is a subclass of int)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) 


def update_despatch_advice(email_id: str, despatch_id: str, body: str):
    """ Retrieves the despatch advice with the corresponding despatch ID if the ID provided is valid and
        and updates the despatch advice document. 

    Args:
        despatch_id: str that indicates the corresponding ID of the despatch advice document to be retrieved
        body: str that indicates the body of the request    

    Returns:
        Response: Response dict with statusCode, Content-Type, and body (XML on success, JSON for errors)
    """

    try:
        body = json.loads(body)

        delivered_quantity = body.get("deliveredQuantity")
        backorder_quantity = body.get("backorderQuantity")
        backorder_reason = body.get("backorderReason")
        note = body.get("note")

        # Validate the parameters in the body of the request
        if delivered_quantity is not None and not _is_numeric(delivered_quantity):
            return build_response(400, JSON_TYPE, "Delivered quantity must be a number.")

        if backorder_quantity is not None and not _is_numeric(backorder_quantity):
            return build_response(400, JSON_TYPE, "Backorder quantity must be a number.")

        if backorder_reason is not None and not isinstance(backorder_reason, str):
            return build_response(400, JSON_TYPE, "Backorder reason must be text.")

        if note is not None and not isinstance(note, str):
            return build_response(400, JSON_TYPE, "Note must be text.")

        response = src.db.dynamodb_table.get_item(
            Key={"email_address": email_id, "despatch_id": despatch_id}
        )

        if 'Item' not in response:
            return build_response(404, JSON_TYPE, f'Despatch advice {despatch_id} not found')

        key = f"dispatches/{despatch_id}.xml"

        try:
            s3_response = s3.s3_client.get_object(
                Bucket=s3.BUCKET_NAME,
                Key=key
            )
            xml_string = s3_response['Body'].read().decode('utf-8')
        except ClientError as e:
            print('Error:', e)
            # S3 retrieval failure (missing object, access denied, etc.)
            return build_response(404, JSON_TYPE, f'Despatch advice {despatch_id} not found')

        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            print('Error:', e)
            return build_response(500, JSON_TYPE, 'Stored despatch document is invalid XML.')

        if note:
            note_el = root.find(f'{{{NS_CBC}}}Note')
            if note_el is None:
                note_el = ET.SubElement(root, f'{{{NS_CBC}}}Note')
            note_el.text = note

        for line in root.findall(f'.//{{{NS_CAC}}}DespatchLine'):
            dq = line.find(f'{{{NS_CBC}}}DeliveredQuantity')
            if dq is not None and delivered_quantity is not None:
                dq.text = str(delivered_quantity)

            if backorder_quantity is not None:
                bq = line.find(f'{{{NS_CBC}}}BackorderQuantity')
                if bq is None:
                    bq = ET.SubElement(line, f'{{{NS_CBC}}}BackorderQuantity')
                bq.text = str(backorder_quantity)

            if backorder_reason:
                br = line.find(f'{{{NS_CBC}}}BackorderReason')
                if br is None:
                    br = ET.SubElement(line, f'{{{NS_CBC}}}BackorderReason')
                br.text = backorder_reason

        updated_xml = ET.tostring(root, encoding="unicode")

        s3.s3_client.put_object(
            Bucket=s3.BUCKET_NAME,
            Key=key,
            Body=updated_xml.encode('utf-8'),
            ContentType='application/xml'
        )

        return build_response(200, XML_TYPE, updated_xml)

    except JSONDecodeError as e:
        return build_response(400, JSON_TYPE, f"Invalid JSON in request body: {e}")

    except ClientError as e:
        print('Error:', e)
        return build_response(503, JSON_TYPE, e.response['Error']['Message'])