import json
import xml.etree.ElementTree as ET
import xmlschema
from datetime import datetime, timedelta
from datetime import date

def generate_despatch(event, context):

    try:
        order_xml_string = event['body']

        ## schema validation -> ensures given document passes required schema
        schema = xmlschema.XMLSchema('schemas/maindoc/UBL-Order-2.4.xsd')
        try:
            schema.validate(order_xml_string)
        except xmlschema.XMLSchemaValidationError as e:
            return {'statusCode': 400, 'body': f'Invalid Order XML: {e}'}

        NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
        NS_UBL = 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2'

        root = ET.fromstring(order_xml_string.encode())
 
        order_id = root.findtext(f'{{{NS_CBC}}}ID') or 'UNKNOWN'
        issue_date = root.findtext(f'{{{NS_CBC}}}IssueDate') or ''
        buyer_customer_party = root.findtext(f'{{{NS_CBC}}}BuyerCustomerParty') or ''
        seller_supplier_party = root.findtext(f'{{{NS_CBC}}}SellerSupplierParty') or ''

        ## delivery date calculation
        delivery_start = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
        delivery_end = (datetime.utcnow() + timedelta(days=2)).strftime('%Y-%m-%d')
        issue_date_today = datetime.utcnow().strftime('%Y-%m-%d')


        da = ET.Element(
            f'{{{NS_UBL}}}DespatchAdvice',
            nsmap={None: NS_UBL, 'cbc': NS_CBC, 'cac': NS_CAC}
        )
 
        # Helper: add cbc child directly to da
        def cbc(tag, text, attribs=None):
            el = ET.SubElement(da, f'{{{NS_CBC}}}{tag}', attrib=attribs or {})
            el.text = text
            return el
 
        # Helper: add cbc child to any parent
        def sub_cbc(parent, tag, text, attribs=None):
            el = ET.SubElement(parent, f'{{{NS_CBC}}}{tag}', attrib=attribs or {})
            el.text = text
            return el
    
        return {
            "statusCode": 200
        }
    

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }