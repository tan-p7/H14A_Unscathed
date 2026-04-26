import pytest
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler


BASE_URL = '/api/despatch'
HEALTH_CHECK_PATH = BASE_URL + '/health'
DESPATCH_ADVICE_PATH = BASE_URL + '/despatch-advice'
INVOICE_PATH = '/api/invoices'

valid_order_str = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Order xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\" xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\" xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Order-2\">\n\t<cbc:UBLVersionID>2.0</cbc:UBLVersionID>\n\t<cbc:CustomizationID>urn:oasis:names:specification:ubl:xpath:Order-2.0:sbs-1.0-draft</cbc:CustomizationID>\n\t<cbc:ProfileID>bpid:urn:oasis:names:draft:bpss:ubl-2-sbs-order-with-simple-response-draft</cbc:ProfileID>\n\t<cbc:ID>AEG012345</cbc:ID>\n\t<cbc:SalesOrderID>CON0095678</cbc:SalesOrderID>\n\t<cbc:CopyIndicator>false</cbc:CopyIndicator>\n\t<cbc:UUID>6E09886B-DC6E-439F-82D1-7CCAC7F4E3B1</cbc:UUID>\n\t<cbc:IssueDate>2005-06-20</cbc:IssueDate>\n\t<cbc:Note>sample</cbc:Note>\n\t<cac:BuyerCustomerParty>\n\t\t<cbc:CustomerAssignedAccountID>XFB01</cbc:CustomerAssignedAccountID>\n\t\t<cbc:SupplierAssignedAccountID>GT00978567</cbc:SupplierAssignedAccountID>\n\t\t<cac:Party>\n\t\t\t<cac:PartyName>\n\t\t\t\t<cbc:Name>IYT Corporation</cbc:Name>\n\t\t\t</cac:PartyName>\n\t\t\t<cac:PostalAddress>\n\t\t\t\t<cbc:StreetName>Avon Way</cbc:StreetName>\n\t\t\t\t<cbc:BuildingName>Thereabouts</cbc:BuildingName>\n\t\t\t\t<cbc:BuildingNumber>56A</cbc:BuildingNumber>\n\t\t\t\t<cbc:CityName>Bridgtow</cbc:CityName>\n\t\t\t\t<cbc:PostalZone>ZZ99 1ZZ</cbc:PostalZone>\n\t\t\t\t<cbc:CountrySubentity>Avon</cbc:CountrySubentity>\n\t\t\t\t<cac:AddressLine>\n\t\t\t\t\t<cbc:Line>3rd Floor, Room 5</cbc:Line>\n\t\t\t\t</cac:AddressLine>\n\t\t\t\t<cac:Country>\n\t\t\t\t\t<cbc:IdentificationCode>GB</cbc:IdentificationCode>\n\t\t\t\t</cac:Country>\n\t\t\t</cac:PostalAddress>\n\t\t\t<cac:PartyTaxScheme>\n\t\t\t\t<cbc:RegistrationName>Bridgtow District Council</cbc:RegistrationName>\n\t\t\t\t<cbc:CompanyID>12356478</cbc:CompanyID>\n\t\t\t\t<cbc:ExemptionReason>Local Authority</cbc:ExemptionReason>\n\t\t\t\t<cac:TaxScheme>\n\t\t\t\t\t<cbc:ID>UK VAT</cbc:ID>\n\t\t\t\t\t<cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>\n\t\t\t\t</cac:TaxScheme>\n\t\t\t</cac:PartyTaxScheme>\n\t\t\t<cac:Contact>\n\t\t\t\t<cbc:Name>Mr Fred Churchill</cbc:Name>\n\t\t\t\t<cbc:Telephone>0127 2653214</cbc:Telephone>\n\t\t\t\t<cbc:Telefax>0127 2653215</cbc:Telefax>\n\t\t\t\t<cbc:ElectronicMail>fred@iytcorporation.gov.uk</cbc:ElectronicMail>\n\t\t\t</cac:Contact>\n\t\t</cac:Party>\n\t</cac:BuyerCustomerParty>\n\t<cac:SellerSupplierParty>\n\t\t<cbc:CustomerAssignedAccountID>CO001</cbc:CustomerAssignedAccountID>\n\t\t<cac:Party>\n\t\t\t<cac:PartyName>\n\t\t\t\t<cbc:Name>Consortial</cbc:Name>\n\t\t\t</cac:PartyName>\n\t\t\t<cac:PostalAddress>\n\t\t\t\t<cbc:StreetName>Busy Street</cbc:StreetName>\n\t\t\t\t<cbc:BuildingName>Thereabouts</cbc:BuildingName>\n\t\t\t\t<cbc:BuildingNumber>56A</cbc:BuildingNumber>\n\t\t\t\t<cbc:CityName>Farthing</cbc:CityName>\n\t\t\t\t<cbc:PostalZone>AA99 1BB</cbc:PostalZone>\n\t\t\t\t<cbc:CountrySubentity>Heremouthshire</cbc:CountrySubentity>\n\t\t\t\t<cac:AddressLine>\n\t\t\t\t\t<cbc:Line>The Roundabout</cbc:Line>\n\t\t\t\t</cac:AddressLine>\n\t\t\t\t<cac:Country>\n\t\t\t\t\t<cbc:IdentificationCode>GB</cbc:IdentificationCode>\n\t\t\t\t</cac:Country>\n\t\t\t</cac:PostalAddress>\n\t\t\t<cac:PartyTaxScheme>\n\t\t\t\t<cbc:RegistrationName>Farthing Purchasing Consortium</cbc:RegistrationName>\n\t\t\t\t<cbc:CompanyID>175 269 2355</cbc:CompanyID>\n\t\t\t\t<cbc:ExemptionReason>N/A</cbc:ExemptionReason>\n\t\t\t\t<cac:TaxScheme>\n\t\t\t\t\t<cbc:ID>VAT</cbc:ID>\n\t\t\t\t\t<cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>\n\t\t\t\t</cac:TaxScheme>\n\t\t\t</cac:PartyTaxScheme>\n\t\t\t<cac:Contact>\n\t\t\t\t<cbc:Name>Mrs Bouquet</cbc:Name>\n\t\t\t\t<cbc:Telephone>0158 1233714</cbc:Telephone>\n\t\t\t\t<cbc:Telefax>0158 1233856</cbc:Telefax>\n\t\t\t\t<cbc:ElectronicMail>bouquet@fpconsortial.co.uk</cbc:ElectronicMail>\n\t\t\t</cac:Contact>\n\t\t</cac:Party>\n\t</cac:SellerSupplierParty>\n\t<cac:OriginatorCustomerParty>\n\t\t<cac:Party>\n\t\t\t<cac:PartyName>\n\t\t\t\t<cbc:Name>The Terminus</cbc:Name>\n\t\t\t</cac:PartyName>\n\t\t\t<cac:PostalAddress>\n\t\t\t\t<cbc:StreetName>Avon Way</cbc:StreetName>\n\t\t\t\t<cbc:BuildingName>Thereabouts</cbc:BuildingName>\n\t\t\t\t<cbc:BuildingNumber>56A</cbc:BuildingNumber>\n\t\t\t\t<cbc:CityName>Bridgtow</cbc:CityName>\n\t\t\t\t<cbc:PostalZone>ZZ99 1ZZ</cbc:PostalZone>\n\t\t\t\t<cbc:CountrySubentity>Avon</cbc:CountrySubentity>\n\t\t\t\t<cac:AddressLine>\n\t\t\t\t\t<cbc:Line>3rd Floor, Room 5</cbc:Line>\n\t\t\t\t</cac:AddressLine>\n\t\t\t\t<cac:Country>\n\t\t\t\t\t<cbc:IdentificationCode>GB</cbc:IdentificationCode>\n\t\t\t\t</cac:Country>\n\t\t\t</cac:PostalAddress>\n\t\t\t<cac:PartyTaxScheme>\n\t\t\t\t<cbc:RegistrationName>Bridgtow District Council</cbc:RegistrationName>\n\t\t\t\t<cbc:CompanyID>12356478</cbc:CompanyID>\n\t\t\t\t<cbc:ExemptionReason>Local Authority</cbc:ExemptionReason>\n\t\t\t\t<cac:TaxScheme>\n\t\t\t\t\t<cbc:ID>UK VAT</cbc:ID>\n\t\t\t\t\t<cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>\n\t\t\t\t</cac:TaxScheme>\n\t\t\t</cac:PartyTaxScheme>\n\t\t\t<cac:Contact>\n\t\t\t\t<cbc:Name>S Massiah</cbc:Name>\n\t\t\t\t<cbc:Telephone>0127 98876545</cbc:Telephone>\n\t\t\t\t<cbc:Telefax>0127 98876546</cbc:Telefax>\n\t\t\t\t<cbc:ElectronicMail>smassiah@the-email.co.uk</cbc:ElectronicMail>\n\t\t\t</cac:Contact>\n\t\t</cac:Party>\n\t</cac:OriginatorCustomerParty>\n\t<cac:Delivery>\n\t\t<cac:DeliveryAddress>\n\t\t\t<cbc:StreetName>Avon Way</cbc:StreetName>\n\t\t\t<cbc:BuildingName>Thereabouts</cbc:BuildingName>\n\t\t\t<cbc:BuildingNumber>56A</cbc:BuildingNumber>\n\t\t\t<cbc:CityName>Bridgtow</cbc:CityName>\n\t\t\t<cbc:PostalZone>ZZ99 1ZZ</cbc:PostalZone>\n\t\t\t<cbc:CountrySubentity>Avon</cbc:CountrySubentity>\n\t\t\t<cac:AddressLine>\n\t\t\t\t<cbc:Line>3rd Floor, Room 5</cbc:Line>\n\t\t\t</cac:AddressLine>\n\t\t\t<cac:Country>\n\t\t\t\t<cbc:IdentificationCode>GB</cbc:IdentificationCode>\n\t\t\t</cac:Country>\n\t\t</cac:DeliveryAddress>\n\t\t<cac:RequestedDeliveryPeriod>\n\t\t\t<cbc:StartDate>2005-06-29</cbc:StartDate>\n\t\t\t<cbc:StartTime>09:30:47.0Z</cbc:StartTime>\n\t\t\t<cbc:EndDate>2005-06-29</cbc:EndDate>\n\t\t\t<cbc:EndTime>09:30:47.0Z</cbc:EndTime>\n\t\t</cac:RequestedDeliveryPeriod>\n\t</cac:Delivery>\n\t<cac:DeliveryTerms>\n\t\t<cbc:SpecialTerms>1% deduction for late delivery as per contract</cbc:SpecialTerms>\n\t</cac:DeliveryTerms>\n\t<cac:TransactionConditions>\n\t\t<cbc:Description>order response required; payment is by BACS or by cheque</cbc:Description>\n\t</cac:TransactionConditions>\n\t<cac:AnticipatedMonetaryTotal>\n\t\t<cbc:LineExtensionAmount currencyID=\"GBP\">100.00</cbc:LineExtensionAmount>\n\t\t<cbc:PayableAmount currencyID=\"GBP\">100.00</cbc:PayableAmount>\n\t</cac:AnticipatedMonetaryTotal>\n\t<cac:OrderLine>\n\t\t<cbc:Note>this is an illustrative order line</cbc:Note>\n\t\t<cac:LineItem>\n\t\t\t<cbc:ID>1</cbc:ID>\n\t\t\t<cbc:SalesOrderID>A</cbc:SalesOrderID>\n\t\t\t<cbc:LineStatusCode>NoStatus</cbc:LineStatusCode>\n\t\t\t<cbc:Quantity unitCode=\"KGM\">100</cbc:Quantity>\n\t\t\t<cbc:LineExtensionAmount currencyID=\"GBP\">100.00</cbc:LineExtensionAmount>\n\t\t\t<cbc:TotalTaxAmount currencyID=\"GBP\">17.50</cbc:TotalTaxAmount>\n\t\t\t<cac:Price>\n\t\t\t\t<cbc:PriceAmount currencyID=\"GBP\">100.00</cbc:PriceAmount>\n\t\t\t\t<cbc:BaseQuantity unitCode=\"KGM\">1</cbc:BaseQuantity>\n\t\t\t</cac:Price>\n\t\t\t<cac:Item>\n\t\t\t\t<cbc:Description>Acme beeswax</cbc:Description>\n\t\t\t\t<cbc:Name>beeswax</cbc:Name>\n\t\t\t\t<cac:BuyersItemIdentification>\n\t\t\t\t\t<cbc:ID>6578489</cbc:ID>\n\t\t\t\t</cac:BuyersItemIdentification>\n\t\t\t\t<cac:SellersItemIdentification>\n\t\t\t\t\t<cbc:ID>17589683</cbc:ID>\n\t\t\t\t</cac:SellersItemIdentification>\n\t\t\t</cac:Item>\n\t\t</cac:LineItem>\n\t</cac:OrderLine>\n</Order>"
valid_despatch_str = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<DespatchAdvice xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\" xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\" xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2\">\n\t<cbc:UBLVersionID>2.0</cbc:UBLVersionID>\n\t<cbc:CustomizationID>urn:oasis:names:specification:ubl:xpath:DespatchAdvice-2.0:sbs-1.0-draft</cbc:CustomizationID>\n\t<cbc:ProfileID>bpid:urn:oasis:names:draft:bpss:ubl-2-sbs-despatch-advice-notification-draft</cbc:ProfileID>\n\t<cbc:ID>565899</cbc:ID>\n\t<cbc:CopyIndicator>false</cbc:CopyIndicator>\n\t<cbc:UUID>88C7280E-8F10-419F-9949-8EFFFA2842B8</cbc:UUID>\n\t<cbc:IssueDate>2005-06-20</cbc:IssueDate>\n\t<cbc:DocumentStatusCode>NoStatus</cbc:DocumentStatusCode>\n\t<cbc:DespatchAdviceTypeCode>delivery</cbc:DespatchAdviceTypeCode>\n\t<cbc:Note>sample</cbc:Note>\n\t<cac:OrderReference>\n\t\t<cbc:ID>AEG012345</cbc:ID>\n\t\t<cbc:SalesOrderID>CON0095678</cbc:SalesOrderID>\n\t\t<cbc:UUID>6E09886B-DC6E-439F-82D1-7CCAC7F4E3B1</cbc:UUID>\n\t\t<cbc:IssueDate>2005-06-20</cbc:IssueDate>\n\t</cac:OrderReference>\n\t...\n</DespatchAdvice>"
valid_invoice_str = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\"\n\txmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\"\n\txmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\">\n  <cbc:ID>123</cbc:ID>\n  <cbc:IssueDate>2011-09-22</cbc:IssueDate>\n  <cac:InvoicePeriod>\n    <cbc:StartDate>2011-08-01</cbc:StartDate>\n    <cbc:EndDate>2011-08-31</cbc:EndDate>\n  </cac:InvoicePeriod>\n  <cac:AccountingSupplierParty>\n    <cac:Party>\n      <cac:PartyName>\n        <cbc:Name>Custom Cotter Pins</cbc:Name>\n      </cac:PartyName>\n    </cac:Party>\n  </cac:AccountingSupplierParty>\n  <cac:AccountingCustomerParty>\n    <cac:Party>\n      <cac:PartyName>\n        <cbc:Name>North American Veeblefetzer</cbc:Name>\n      </cac:PartyName>\n    </cac:Party>\n  </cac:AccountingCustomerParty>\n  <cac:LegalMonetaryTotal>\n     <cbc:PayableAmount currencyID=\"CAD\">100.00</cbc:PayableAmount>\n  </cac:LegalMonetaryTotal>\n  <cac:InvoiceLine>\n    <cbc:ID>1</cbc:ID>\n    <cbc:LineExtensionAmount currencyID=\"CAD\">100.00</cbc:LineExtensionAmount>\n    <cac:Item>\n       <cbc:Description>Cotter pin, MIL-SPEC</cbc:Description>\n    </cac:Item>\n  </cac:InvoiceLine>\n</Invoice>"
invalid_xml = "this is not an xml"

def make_event(method, path, path_params=None, body=None, headers=None):
    event = {
        'httpMethod': method,
        'path': path,
        'pathParameters': path_params
    }
    if body is not None:
        event['body'] = body
    if headers is not None:
        event['headers'] = headers
    return event



class TestLambdaHealthCheckRoute:
    @patch('src.lambda_function.health_check')
    def test_get_health_check_routes_correctly(self, mock_health):
        mock_health.return_value = {'statusCode': 200}
        response = lambda_handler(make_event('GET', HEALTH_CHECK_PATH), {})
        mock_health.assert_called_once()
        assert response['statusCode'] == 200



class TestLambdaRetrieveAll:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_get_all_despatch_returns_response(self, mock_retrieve, _mock_auth):
        mock_retrieve.return_value = {'statusCode': 200}
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        mock_retrieve.assert_called_once_with("user@example.com")
        assert response['statusCode'] == 200


class TestLambdaGenerateDespatch:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.generate_despatch')
    def test_post_despatch_advice_calls_generate_with_body(self, mock_generate, _mock_auth):
        mock_generate.return_value = {'statusCode': 200}
        body = '<Order xmlns="urn:oasis:names:specification:ubl:schema:xsd:Order-2">...</Order>'
        response = lambda_handler(make_event('POST', DESPATCH_ADVICE_PATH, body=body), {})
        mock_generate.assert_called_once_with(body, "user@example.com")
        assert response['statusCode'] == 200

    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.generate_despatch')
    def test_post_despatch_advice_passes_empty_string_when_no_body(self, mock_generate, _mock_auth):
        mock_generate.return_value = {'statusCode': 400}
        response = lambda_handler(make_event('POST', DESPATCH_ADVICE_PATH), {})
        mock_generate.assert_called_once_with('', "user@example.com")
        assert response['statusCode'] == 400


class TestLambdaRetrieveDespatchById:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.retrieve_despatch')
    def test_get_despatch_by_id_calls_retrieve_with_despatch_id(self, mock_retrieve, _mock_auth):
        mock_retrieve.return_value = {'statusCode': 200}
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('GET', path, path_params={'despatch-id': '12345'}),
            {}
        )
        mock_retrieve.assert_called_once_with("user@example.com", '12345')
        assert response['statusCode'] == 200

    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.retrieve_despatch')
    def test_get_despatch_by_id_returns_404_when_despatch_id_missing(self, mock_retrieve, _mock_auth):
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('GET', path, path_params={'despatch-id': None}),
            {}
        )
        mock_retrieve.assert_not_called()
        assert response['statusCode'] == 404


class TestLambdaUpdateDespatch:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.update_despatch_advice')
    def test_put_despatch_advice_calls_update_with_id_and_body(self, mock_update, _mock_auth):
        mock_update.return_value = {'statusCode': 200}
        path = DESPATCH_ADVICE_PATH + '/999'
        body = '{"deliveredQuantity": 5}'
        response = lambda_handler(
            make_event('PUT', path, path_params={'despatch-id': '999'}, body=body),
            {}
        )
        mock_update.assert_called_once_with("user@example.com", '999', body)
        assert response['statusCode'] == 200

    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.update_despatch_advice')
    def test_put_despatch_advice_passes_empty_json_when_no_body(self, mock_update, _mock_auth):
        mock_update.return_value = {'statusCode': 200}
        path = DESPATCH_ADVICE_PATH + '/999'
        response = lambda_handler(
            make_event('PUT', path, path_params={'despatch-id': '999'}),
            {}
        )
        mock_update.assert_called_once_with("user@example.com", '999', '{}')
        assert response['statusCode'] == 200

    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.update_despatch_advice')
    def test_put_despatch_returns_404_when_despatch_id_missing(self, mock_update, _mock_auth):
        path = DESPATCH_ADVICE_PATH + '/999'
        response = lambda_handler(
            make_event('PUT', path, path_params={'despatch-id': None}),
            {}
        )
        mock_update.assert_not_called()
        assert response['statusCode'] == 404


class TestLambdaDeleteDespatch:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.delete_despatch')
    def test_delete_despatch_by_id_calls_delete_with_despatch_id(self, mock_delete, _mock_auth):
        mock_delete.return_value = {'statusCode': 204}
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('DELETE', path, path_params={'despatch-id': '12345'}),
            {}
        )
        mock_delete.assert_called_once_with("user@example.com", '12345')
        assert response['statusCode'] == 204

    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.delete_despatch')
    def test_delete_despatch_returns_404_when_despatch_id_missing(self, mock_delete, _mock_auth):
        path = DESPATCH_ADVICE_PATH + '/12345'
        response = lambda_handler(
            make_event('DELETE', path, path_params={'despatch-id': None}),
            {}
        )
        mock_delete.assert_not_called()
        assert response['statusCode'] == 404


class TestLambdaNotFound:
    def test_unknown_path_returns_404(self):
        response = lambda_handler(make_event('POST', HEALTH_CHECK_PATH), {})
        assert response['statusCode'] == 404


class TestLambdaExceptionHandling:
    @patch('src.lambda_function.get_auth_context', return_value=({"sub": "u1", "email": "user@example.com"}, None))
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_exception_returns_500(self, mock_retrieve, _mock_auth):
        mock_retrieve.side_effect = Exception('Unexpected error')
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        assert response['statusCode'] == 500


class TestLambdaAuthRoutes:
    @patch('src.lambda_function.register')
    def test_post_register_routes_to_register(self, mock_register):
        mock_register.return_value = {'statusCode': 201}
        response = lambda_handler(
            make_event('POST', '/api/auth/register', body='{}'),
            {}
        )
        mock_register.assert_called_once()
        assert response['statusCode'] == 201

    @patch('src.lambda_function.login')
    def test_post_login_routes_to_login(self, mock_login):
        mock_login.return_value = {'statusCode': 200}
        response = lambda_handler(
            make_event('POST', '/api/auth/login', body='{}'),
            {}
        )
        mock_login.assert_called_once()
        assert response['statusCode'] == 200

    @patch('src.lambda_function.logout')
    def test_post_logout_routes_to_logout(self, mock_logout):
        mock_logout.return_value = {'statusCode': 204}
        response = lambda_handler(
            make_event('POST', '/api/auth/logout'),
            {}
        )
        mock_logout.assert_called_once()
        assert response['statusCode'] == 204


class TestLambdaCorsOptions:
    def test_options_despatch_returns_204(self):
        response = lambda_handler(
            make_event('OPTIONS', DESPATCH_ADVICE_PATH),
            {}
        )
        assert response['statusCode'] == 204

    def test_options_auth_returns_204(self):
        response = lambda_handler(
            make_event('OPTIONS', '/api/auth/register'),
            {}
        )
        assert response['statusCode'] == 204


class TestLambdaDespatchRequiresAuth:
    @patch('src.lambda_function.retrieve_all_despatch_advice')
    def test_get_all_without_token_returns_401(self, mock_retrieve):
        response = lambda_handler(make_event('GET', DESPATCH_ADVICE_PATH), {})
        mock_retrieve.assert_not_called()
        assert response['statusCode'] == 401

# Test Invoice Endpoints
#class TestLambdaCreateInvoice:
#    @patch('src.lambda_function.createInvoice')
#    def test_post_invoice_routes_correctly(self, mock_create):
#        mock_create.return_value = {'statusCode': 201}
#        response = lambda_handler(make_event('POST', INVOICE_PATH), {})
#        mock_create.assert_called_once()
#        assert response['statusCode'] == 201


#class TestLambdaRetrieveInvoice:
#    @patch('src.lambda_function.retrieveInvoiceById')
#    def test_get_invoice_by_id_routes_correctly(self, mock_retrieve):
#        mock_retrieve.return_value = {'statusCode': 200}
#        response = lambda_handler(make_event('GET', f'{INVOICE_PATH}/INV-123', path_params={'invoice_id': 'INV-123'}), {})
#        mock_retrieve.assert_called_once_with('INV-123')
#        assert response['statusCode'] == 200


#class TestLambdaUpdateInvoice:
#    @patch('src.lambda_function.updateInvoiceById')
#    def test_put_invoice_routes_correctly(self, mock_update):
#        mock_update.return_value = {'statusCode': 200}
#        response = lambda_handler(make_event('PUT', f'{INVOICE_PATH}/INV-123', path_params={'invoice_id': 'INV-123'}), {})
#        mock_update.assert_called_once_with('INV-123')
#        assert response['statusCode'] == 200


#class TestLambdaDeleteInvoice:
#    @patch('src.lambda_function.deleteInvoiceById')
#    def test_delete_invoice_routes_correctly(self, mock_delete):
#        mock_delete.return_value = {'statusCode': 200}
#        response = lambda_handler(make_event('DELETE', f'{INVOICE_PATH}/INV-123', path_params={'invoice_id': 'INV-123'}), {})
#        mock_delete.assert_called_once_with('INV-123')
#        assert response['statusCode'] == 204


#class TestLambdaInvoiceStatus:
#    @patch('src.lambda_function.ChangeInvoiceStatus')
#    def test_post_invoice_status_routes_correctly(self, mock_status):
#        mock_status.return_value = {'statusCode': 200}
#        response = lambda_handler(make_event('POST', f'{INVOICE_PATH}/INV-123/status', path_params={'invoice_id': 'INV-123'}), {})
#        mock_status.assert_called_once_with('INV-123')
#        assert response['statusCode'] == 200


#class TestLambdaCreateCreditNote:
#    @patch('src.lambda_function.createCreditNote')
#    def test_post_credit_note_routes_correctly(self, mock_credit):
#        mock_credit.return_value = {'statusCode': 201}
#        response = lambda_handler(make_event('POST', f'{INVOICE_PATH}/INV-123/credit-notes', path_params={'invoice_id': 'INV-123'}), {})
#        mock_credit.assert_called_once_with('INV-123')
#        assert response['statusCode'] == 201


#class TestLambdaInvoiceToPdf:
#    @patch('src.lambda_function.InvoiceToPdf')
#    def test_get_invoice_pdf_routes_correctly(self, mock_pdf):
#        mock_pdf.return_value = {'statusCode': 200}
#        response = lambda_handler(make_event('GET', f'{INVOICE_PATH}/INV-123/pdf', path_params={'invoice_id': 'INV-123'}), {})
#        mock_pdf.assert_called_once_with('INV-123')
#        assert response['statusCode'] == 200

class TestLambdaValidateOrder:
    @patch('src.lambda_function.validate_order')
    def test_validate_order_is_called(self, mock_order_validate):
        mock_order_validate.return_value = { 'statusCode': 200 }

        path = '/api/validate/order'
        response = lambda_handler(
            make_event('POST', path, path_params={}, body=valid_order_str),
            {}
        )
        mock_order_validate.assert_called_once()
        assert response['statusCode'] == 200

class TestLambdaValidateDespatch:
    @patch('src.lambda_function.validate_despatch')
    def test_validate_order_is_called(self, mock_despatch_validate):
        mock_despatch_validate.return_value = { 'statusCode': 200 }

        path = '/api/validate/despatch'
        response = lambda_handler(
            make_event('POST', path, path_params={}, body=valid_despatch_str),
            {}
        )
        mock_despatch_validate.assert_called_once()
        assert response['statusCode'] == 200

class TestLambdaValidateInvoice:
    @patch('src.lambda_function.validate_invoice')
    def test_validate_invoice_is_called(self, mock_invoice_validate):
        mock_invoice_validate.return_value = { 'statusCode': 200 }

        path = '/api/validate/invoice'
        response = lambda_handler(
            make_event('POST', path, path_params={}, body=valid_invoice_str),
            {}
        )
        mock_invoice_validate.assert_called_once()
        assert response['statusCode'] == 200
