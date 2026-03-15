import json
import xml.etree.ElementTree as ET
import xmlschema
import uuid
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from src.helper_functions import build_response
from src.constants import JSON_TYPE, XML_TYPE
from src.db import dynamodb_table

## NAMESPACES!!
NS_CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
NS_CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'
NS_UBL = 'urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2'


def cbc_add(parent, tag, text, attribs=None):
    el = ET.SubElement(parent, f'{{{NS_CBC}}}{tag}', attrib=attribs or {})
    el.text = text
    return el
 
 
def cac_add(parent, tag):
    """
    Add a CommonAggregateComponents child element to a parent.
    e.g. cac_add(da, 'OrderReference') produces <cac:OrderReference>
    """
    return ET.SubElement(parent, f'{{{NS_CAC}}}{tag}')


def append_address(parent, addr: dict):
    """
    Append UBL address fields to a parent element.
    Skips any fields not present in the dict.
    """
    if addr.get('streetName'):       cbc_add(parent, 'StreetName',       addr['streetName'])
    if addr.get('buildingName'):     cbc_add(parent, 'BuildingName',     addr['buildingName'])
    if addr.get('buildingNumber'):   cbc_add(parent, 'BuildingNumber',   addr['buildingNumber'])
    if addr.get('cityName'):         cbc_add(parent, 'CityName',         addr['cityName'])
    if addr.get('postalZone'):       cbc_add(parent, 'PostalZone',       addr['postalZone'])
    if addr.get('countrySubentity'): cbc_add(parent, 'CountrySubentity', addr['countrySubentity'])
    if addr.get('addressLine'):
        al = cac_add(parent, 'AddressLine')
        cbc_add(al, 'Line', addr['addressLine'])
    if addr.get('countryCode'):
        c = cac_add(parent, 'Country')
        cbc_add(c, 'IdentificationCode', addr['countryCode'])

def _party_el_to_dict(party_el):
    """
    Convert a UBL Party XML element to a dict suitable for append_party.
    Returns an empty dict if party_el is None.
    """
    if party_el is None:
        return {}
    addr_el = party_el.find(f'{{{NS_CAC}}}PostalAddress')
    address = None
    if addr_el is not None:
        address = {
            'streetName':       addr_el.findtext(f'{{{NS_CBC}}}StreetName') or None,
            'buildingName':     addr_el.findtext(f'{{{NS_CBC}}}BuildingName') or None,
            'buildingNumber':   addr_el.findtext(f'{{{NS_CBC}}}BuildingNumber') or None,
            'cityName':         addr_el.findtext(f'{{{NS_CBC}}}CityName') or None,
            'postalZone':       addr_el.findtext(f'{{{NS_CBC}}}PostalZone') or None,
            'countrySubentity': addr_el.findtext(f'{{{NS_CBC}}}CountrySubentity') or None,
            'addressLine':      addr_el.findtext(f'{{{NS_CAC}}}AddressLine/{{{NS_CBC}}}Line') or None,
            'countryCode':      addr_el.findtext(f'{{{NS_CAC}}}Country/{{{NS_CBC}}}IdentificationCode') or None,
        }
    tax_el = party_el.find(f'{{{NS_CAC}}}PartyTaxScheme')
    tax_scheme = None
    if tax_el is not None:
        ts_el = tax_el.find(f'{{{NS_CAC}}}TaxScheme')
        tax_scheme = {
            'registrationName': tax_el.findtext(f'{{{NS_CBC}}}RegistrationName') or None,
            'companyID':        tax_el.findtext(f'{{{NS_CBC}}}CompanyID') or None,
            'exemptionReason':  tax_el.findtext(f'{{{NS_CBC}}}ExemptionReason') or None,
            'schemeID':         ts_el.findtext(f'{{{NS_CBC}}}ID') if ts_el is not None else 'VAT',
            'taxTypeCode':      ts_el.findtext(f'{{{NS_CBC}}}TaxTypeCode') if ts_el is not None else 'VAT',
        }
    contact_el = party_el.find(f'{{{NS_CAC}}}Contact')
    contact = None
    if contact_el is not None:
        contact = {
            'name':      contact_el.findtext(f'{{{NS_CBC}}}Name') or None,
            'telephone': contact_el.findtext(f'{{{NS_CBC}}}Telephone') or None,
            'telefax':   contact_el.findtext(f'{{{NS_CBC}}}Telefax') or None,
            'email':     contact_el.findtext(f'{{{NS_CBC}}}ElectronicMail') or None,
        }
    name_el = party_el.find(f'{{{NS_CAC}}}PartyName')
    name = name_el.findtext(f'{{{NS_CBC}}}Name') if name_el is not None else None
    return {
        'name':     name,
        'address':  address,
        'taxScheme': tax_scheme,
        'contact':  contact,
    }


def append_party(parent, party: dict):
    """
    Append a full UBL Party block to a parent element.
    Covers name, postal address, tax scheme, and contact.
    """
    party_el = cac_add(parent, 'Party')
 
    if party.get('name'):
        pn = cac_add(party_el, 'PartyName')
        cbc_add(pn, 'Name', party['name'])
 
    if party.get('address'):
        pa = cac_add(party_el, 'PostalAddress')
        append_address(pa, party['address'])
 
    if party.get('taxScheme'):
        tax = party['taxScheme']
        pts = cac_add(party_el, 'PartyTaxScheme')
        if tax.get('registrationName'): cbc_add(pts, 'RegistrationName', tax['registrationName'])
        if tax.get('companyID'):        cbc_add(pts, 'CompanyID',        tax['companyID'])
        if tax.get('exemptionReason'):  cbc_add(pts, 'ExemptionReason',  tax['exemptionReason'])
        ts = cac_add(pts, 'TaxScheme')
        cbc_add(ts, 'ID',          tax.get('schemeID',    'VAT'))
        cbc_add(ts, 'TaxTypeCode', tax.get('taxTypeCode', 'VAT'))
 
    if party.get('contact'):
        contact = party['contact']
        ce = cac_add(party_el, 'Contact')
        if contact.get('name'):      cbc_add(ce, 'Name',           contact['name'])
        if contact.get('telephone'): cbc_add(ce, 'Telephone',      contact['telephone'])
        if contact.get('telefax'):   cbc_add(ce, 'Telefax',        contact['telefax'])
        if contact.get('email'):     cbc_add(ce, 'ElectronicMail', contact['email'])
 
def generate_despatch(event, context):

    try:
        order_xml_string = event['body']

        ## schema validation -> ensures given document passes required schema
        schema = xmlschema.XMLSchema('schemas/maindoc/UBL-Order-2.4.xsd')
        try:
            schema.validate(order_xml_string)
        except xmlschema.XMLSchemaValidationError as e:
            return build_response(400, JSON_TYPE, f'Invalid Order XML: {e}')


        root = ET.fromstring(order_xml_string.encode())
 
        order_id = root.findtext(f'{{{NS_CBC}}}ID') or 'UNKNOWN'
        issue_date = root.findtext(f'{{{NS_CBC}}}IssueDate') or ''
        sales_order_id = root.findtext(f'.//{{{NS_CAC}}}OrderReference/{{{NS_CBC}}}SalesOrderID') or ''
        order_uuid     = root.findtext(f'.//{{{NS_CAC}}}OrderReference/{{{NS_CBC}}}UUID') or ''

        # Buyer 
        buyer_el       = root.find(f'{{{NS_CAC}}}BuyerCustomerParty')
        buyer_party_el = buyer_el.find(f'{{{NS_CAC}}}Party') if buyer_el is not None else None
        buyer_account_id          = buyer_el.findtext(f'{{{NS_CBC}}}CustomerAssignedAccountID') if buyer_el is not None else ''
        buyer_supplier_account_id = buyer_el.findtext(f'{{{NS_CBC}}}SupplierAssignedAccountID') if buyer_el is not None else ''
 
        # Supplier 
        supplier_el       = root.find(f'{{{NS_CAC}}}SellerSupplierParty')
        supplier_party_el = supplier_el.find(f'{{{NS_CAC}}}Party') if supplier_el is not None else None
        supplier_account_id = supplier_el.findtext(f'{{{NS_CBC}}}CustomerAssignedAccountID') if supplier_el is not None else ''
 
        # Delivery address 
        delivery_el      = root.find(f'{{{NS_CAC}}}Delivery')
        delivery_addr_el = delivery_el.find(f'{{{NS_CAC}}}DeliveryAddress') if delivery_el is not None else None
        if delivery_addr_el is None and buyer_party_el is not None:
            delivery_addr_el = buyer_party_el.find(f'.//{{{NS_CAC}}}PostalAddress')
        delivery_address = {
            'streetName':       delivery_addr_el.findtext(f'{{{NS_CBC}}}StreetName')       if delivery_addr_el is not None else None,
            'buildingName':     delivery_addr_el.findtext(f'{{{NS_CBC}}}BuildingName')     if delivery_addr_el is not None else None,
            'buildingNumber':   delivery_addr_el.findtext(f'{{{NS_CBC}}}BuildingNumber')   if delivery_addr_el is not None else None,
            'cityName':         delivery_addr_el.findtext(f'{{{NS_CBC}}}CityName')         if delivery_addr_el is not None else None,
            'postalZone':       delivery_addr_el.findtext(f'{{{NS_CBC}}}PostalZone')       if delivery_addr_el is not None else None,
            'countrySubentity': delivery_addr_el.findtext(f'{{{NS_CBC}}}CountrySubentity') if delivery_addr_el is not None else None,
            'addressLine':      delivery_addr_el.findtext(f'{{{NS_CAC}}}AddressLine/{{{NS_CBC}}}Line') if delivery_addr_el is not None else None,
            'countryCode':      delivery_addr_el.findtext(f'{{{NS_CAC}}}Country/{{{NS_CBC}}}IdentificationCode') if delivery_addr_el is not None else None,
        }

        ## delivery date calculation
        delivery_start = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
        delivery_end = (datetime.utcnow() + timedelta(days=2)).strftime('%Y-%m-%d')
        issue_date_today = datetime.utcnow().strftime('%Y-%m-%d')

        # Order lines
        lines = []
        for line in root.findall(f'.//{{{NS_CAC}}}OrderLine'):
            line_item = line.find(f'{{{NS_CAC}}}LineItem')
            item_el   = line.find(f'.//{{{NS_CAC}}}Item')
            qty_el    = line_item.find(f'{{{NS_CBC}}}Quantity') if line_item is not None else None
            lines.append({
                'lineID':          line_item.findtext(f'{{{NS_CBC}}}ID') if line_item is not None else str(len(lines) + 1),
                'quantity':        qty_el.text                if qty_el is not None else '0',
                'unitCode':        qty_el.get('unitCode','EA') if qty_el is not None else 'EA',
                'itemDescription': item_el.findtext(f'{{{NS_CBC}}}Description') if item_el is not None else '',
                'itemName':        item_el.findtext(f'{{{NS_CBC}}}Name')        if item_el is not None else '',
                'buyersItemID':    item_el.findtext(f'.//{{{NS_CAC}}}BuyersItemIdentification/{{{NS_CBC}}}ID')  if item_el is not None else '',
                'sellersItemID':   item_el.findtext(f'.//{{{NS_CAC}}}SellersItemIdentification/{{{NS_CBC}}}ID') if item_el is not None else '',
            })

        ## WHAT ARE WE DOING FOR ADDRESSES
        ## building our XML
        da = ET.Element(f'{{{NS_UBL}}}DespatchAdvice')


        # Use a string despatch_id to match DynamoDB partition key type
        despatch_id = str(uuid.uuid4().int)[:9]
        cbc_add(da, 'UBLVersionID',          '2.0')
        cbc_add(da, 'CustomizationID',       'urn:oasis:names:specification:ubl:xpath:DespatchAdvice-2.0:sbs-1.0-draft')
        cbc_add(da, 'ProfileID',             'bpid:urn:oasis:names:draft:bpss:ubl-2-sbs-despatch-advice-notification-draft')
        cbc_add(da, 'ID',                    despatch_id)
        cbc_add(da, 'CopyIndicator',         'false')
        cbc_add(da, 'UUID',                  str(uuid.uuid4()).upper())
        cbc_add(da, 'IssueDate',             issue_date_today)
        cbc_add(da, 'DocumentStatusCode',    'NoStatus')
        cbc_add(da, 'DespatchAdviceTypeCode','delivery')
 
        # -- <cac:OrderReference> --
        # Links this despatch back to the original order
        order_ref = cac_add(da, 'OrderReference')
        cbc_add(order_ref, 'ID', order_id)
        cbc_add(order_ref, 'SalesOrderID', sales_order_id)
        cbc_add(order_ref, 'IssueDate', issue_date)
        cbc_add(order_ref, 'UUID', order_uuid)


        # -- <cac:DespatchSupplierParty> --
        # The supplier who is sending the goods
        dsp = cac_add(da, 'DespatchSupplierParty')
        if supplier_account_id:
            cbc_add(dsp, 'CustomerAssignedAccountID', supplier_account_id)
        append_party(dsp, _party_el_to_dict(supplier_party_el))

        # -- <cac:DeliveryCustomerParty> --
        # The customer who is receiving the goods
        dcp = cac_add(da, 'DeliveryCustomerParty')
        
        cbc_add(dcp, 'CustomerAssignedAccountID', buyer_account_id)

        if buyer_supplier_account_id:
            cbc_add(dcp, 'SupplierAssignedAccountID', buyer_supplier_account_id)
        append_party(dcp, _party_el_to_dict(buyer_party_el))
 
        # <cac:Shipment> — delivery address and delivery window
        shipment    = cac_add(da, 'Shipment')
        cbc_add(shipment, 'ID', '1')
        consignment = cac_add(shipment, 'Consignment')
        cbc_add(consignment, 'ID', '1')
        delivery    = cac_add(shipment, 'Delivery')
        da_addr     = cac_add(delivery, 'DeliveryAddress')
        append_address(da_addr, delivery_address)
        rdp = cac_add(delivery, 'RequestedDeliveryPeriod')
        cbc_add(rdp, 'StartDate', delivery_start)
        cbc_add(rdp, 'EndDate',   delivery_end)
 
        # <cac:DespatchLine> — one per order line
        for i, line in enumerate(lines, start=1):
            dl = cac_add(da, 'DespatchLine')
            cbc_add(dl, 'ID',                str(i))
            cbc_add(dl, 'LineStatusCode',    'NoStatus')
            cbc_add(dl, 'DeliveredQuantity', line['quantity'], {'unitCode': line['unitCode']})
 
            # Link back to the original order line
            olr = cac_add(dl, 'OrderLineReference')
            cbc_add(olr, 'LineID', line['lineID'])
            ior = cac_add(olr, 'OrderReference')
            cbc_add(ior, 'ID', order_id)
            cbc_add(ior, 'SalesOrderID', sales_order_id)
            cbc_add(ior, 'UUID', order_uuid)
            if issue_date:
                cbc_add(ior, 'IssueDate', issue_date)
 
            # Item details
            item = cac_add(dl, 'Item')
            if line.get('itemDescription'): cbc_add(item, 'Description', line['itemDescription'])
            if line.get('itemName'):        cbc_add(item, 'Name',        line['itemName'])
            if line.get('buyersItemID'):
                bid = cac_add(item, 'BuyersItemIdentification')
                cbc_add(bid, 'ID', line['buyersItemID'])
            if line.get('sellersItemID'):
                sid = cac_add(item, 'SellersItemIdentification')
                cbc_add(sid, 'ID', line['sellersItemID'])
 
        # Store in DynamoDB and return
        despatch_xml = ET.tostring(da, encoding='unicode')
        try:
            dynamodb_table.put_item(
                Item={
                    'despatch_id': despatch_id,
                    'despatch_ubl': despatch_xml,
                }
            )
        except ClientError as e:
            print('Error:', e)
            return build_response(400, JSON_TYPE, e.response['Error']['Message'])

        return build_response(200, XML_TYPE, despatch_xml)

    except Exception as e:
        return build_response(400, JSON_TYPE, str(e))
    
