""" 
import json
from src.invoice_handling import createInvoice, retrieveInvoiceById, updateInvoiceById, deleteInvoiceById, createCreditNote, InvoiceStatus, InvoiceToPdf

class Test:
    def test_invoice_v1(self):
        # create invoice
        createInvoiceResponse = createInvoice()
        print(createInvoice[status])
        assert createInvoiceResponse["statusCode"] == 201
        invoice_id = (createInvoiceResponse['body'])['invoice']['invoice_id']
        assert invoice_id is not None

        retrieveInvoiceResponse = retrieveInvoiceById(invoice_id)
        assert retrieveInvoiceResponse["statusCode"] == 200

        updateInvoiceResponse = updateInvoiceById(invoice_id)
        assert updateInvoiceResponse["statusCode"] == 200

        updateInvoiceStatus = InvoiceStatus(invoice_id)
        assert updateInvoiceStatus["statusCode"] == 200
        
        createCreditNoteResponse = createCreditNote(invoice_id)
        assert createCreditNoteResponse["statusCode"] == 201

        ConvertInvoiceToPdf = InvoiceToPdf(invoice_id)
        assert ConvertInvoiceToPdf["statusCode"] == 200

    def test_invoice_v2(self):

        createInvoiceResponse = createInvoice()
        assert createInvoiceResponse["statusCode"] == 201
        invoice_id = (createInvoiceResponse['body'])['invoice']['invoice_id']
        assert invoice_id is not None
    
        deleteInvoiceResponse = deleteInvoiceById(invoice_id)
        assert deleteInvoiceResponse["statusCode"] == 204
 """