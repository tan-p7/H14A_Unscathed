import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

const API = import.meta.env.VITE_API_URL ?? '/atlas'

const STANDARDS = [
    { code: 'AU', label: 'Australia / New Zealand', standard: 'PEPPOL BIS Billing 3.0', description: 'Required for Australian and New Zealand government invoicing, broadly used across industries' },
    { code: 'SG', label: 'Singapore', standard: 'InvoiceNow (PEPPOL)', description: "InvoiceNow is Singapore's national e-invoicing network, built on PEPPOL" },
    { code: 'JP', label: 'Japan', standard: 'JP PINT', description: 'Japan Procurement INTeroperability - mandatory for Japanese government procurement since 2023' },
    { code: 'EU', label: 'European Union', standard: 'EN 16931', description: 'EU directive 2014/55/EU requires this standard for public sector invoicing' },
    { code: 'US', label: 'United States', standard: 'UBL 2.1', description: 'No federal mandate yet, but UBL 2.1 is the most widely accepted format' },
]

const TAX_SCHEME_BY_COUNTRY = {
    AU: 'GST', SG: 'GST', JP: 'JCT', EU: 'VAT', US: 'Sales Tax'
}

const CURRENCY_BY_COUNTRY = {
    AU: 'AUD', SG: 'SGD', JP: 'JPY', EU: 'EUR', US: 'USD'
}

const DEFAULT_TAX_BY_COUNTRY = {
    AU: '10', SG: '9', JP: '10', EU: '20', US: '0'
}

const PAYMENT_FIELD_LABELS = {
    AU: { account: 'Bank Account Number', branch: 'BSB' },
    SG: { account: 'Bank Account Number', branch: 'Bank Code' },
    JP: { account: 'Bank Account Number', branch: 'Branch Code' },
    EU: { account: 'IBAN', branch: 'BIC / SWIFT' },
    US: { account: 'Account Number', branch: 'Routing Number' },
}

export default function GenerateInvoice() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [step, setStep] = useState(1)
    const [selectedStandard, setSelectedStandard] = useState(null)
    const [formatted, setFormatted] = useState(null)
    const [loading, setLoading] = useState(true)
    const [generatedXml, setGeneratedXml] = useState(null)
    const [showRaw, setShowRaw] = useState(false)
    const [saving, setSaving] = useState(false)
    const [saveError, setSaveError] = useState('')

    const year = new Date().getFullYear()
    const seq = String(Math.floor(Math.random() * 900) + 100)
    const [invoiceNumber, setInvoiceNumber] = useState(`INV-${year}-${seq}`)
    const [issueDate, setIssueDate] = useState(new Date().toISOString().split('T')[0])
    const [dueDate, setDueDate] = useState(new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])
    const [taxRate, setTaxRate] = useState('10')
    const [paymentTerms, setPaymentTerms] = useState('Net 30')
    const [bankAccount, setBankAccount] = useState('')
    const [branchCode, setBranchCode] = useState('')
    const [note, setNote] = useState('')
    const [unitPrice, setUnitPrice] = useState('')
    const [currency, setCurrency] = useState('AUD')

    useEffect(() => {
        const fetchDespatch = async () => {
            const token = localStorage.getItem('accessToken')
            const response = await fetch(`${API}/api/despatch/despatch-advice/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            const data = await response.text()
            const parser = new DOMParser()
            const doc = parser.parseFromString(data, 'application/xml')
            const getTag = (tag) => doc.getElementsByTagName(tag)[0]?.textContent || ''

            setFormatted({
                id: getTag('ns1:ID'),
                issueDate: getTag('ns1:IssueDate'),
                orderRef: doc.getElementsByTagName('ns2:OrderReference')[0]?.getElementsByTagName('ns1:ID')[0]?.textContent || '',
                supplier: doc.getElementsByTagName('ns2:DespatchSupplierParty')[0]?.getElementsByTagName('ns1:Name')[0]?.textContent || '',
                customer: doc.getElementsByTagName('ns2:DeliveryCustomerParty')[0]?.getElementsByTagName('ns1:Name')[0]?.textContent || '',
                street: getTag('ns1:StreetName'),
                city: getTag('ns1:CityName'),
                postal: getTag('ns1:PostalZone'),
                quantity: getTag('ns1:DeliveredQuantity') || '1',
            })
            setLoading(false)
        }
        fetchDespatch()
    }, [id])

    useEffect(() => {
        if (selectedStandard) {
            setCurrency(CURRENCY_BY_COUNTRY[selectedStandard] || 'AUD')
            setTaxRate(DEFAULT_TAX_BY_COUNTRY[selectedStandard] || '10')
        }
    }, [selectedStandard])

    const stepClass = (index) => {
        if (step > index + 1) return 'bg-green-500 text-white'
        if (step === index + 1) return 'bg-deep-sky-blue-600 text-white'
        return 'bg-gray-200 text-gray-500'
    }

    const standard = STANDARDS.find(s => s.code === selectedStandard)
    const taxScheme = TAX_SCHEME_BY_COUNTRY[selectedStandard] || 'GST'
    const paymentLabels = PAYMENT_FIELD_LABELS[selectedStandard] || PAYMENT_FIELD_LABELS.AU
    const qty = parseFloat(formatted?.quantity) || 1
    const subtotal = qty * (parseFloat(unitPrice) || 0)
    const tax = subtotal * (parseFloat(taxRate) / 100)
    const total = subtotal + tax
    const canGenerate = invoiceNumber && issueDate && dueDate && unitPrice && parseFloat(unitPrice) > 0

    const handleGenerate = () => {
        const xml = `<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
    xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
    xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2">
    <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
    <cbc:CustomizationID>${standard?.standard}</cbc:CustomizationID>
    <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
    <cbc:ID>${invoiceNumber}</cbc:ID>
    <cbc:IssueDate>${issueDate}</cbc:IssueDate>
    <cbc:DueDate>${dueDate}</cbc:DueDate>
    <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
    ${note ? `<cbc:Note>${note}</cbc:Note>` : ''}
    <cbc:DocumentCurrencyCode>${currency}</cbc:DocumentCurrencyCode>
    <cac:OrderReference>
        <cbc:ID>${formatted?.orderRef || ''}</cbc:ID>
    </cac:OrderReference>
    <cac:DespatchDocumentReference>
        <cbc:ID>${id}</cbc:ID>
    </cac:DespatchDocumentReference>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyName>
                <cbc:Name>${formatted?.supplier || ''}</cbc:Name>
            </cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>${formatted?.street || ''}</cbc:StreetName>
                <cbc:CityName>${formatted?.city || ''}</cbc:CityName>
                <cbc:PostalZone>${formatted?.postal || ''}</cbc:PostalZone>
                <cac:Country>
                    <cbc:IdentificationCode>${selectedStandard}</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyName>
                <cbc:Name>${formatted?.customer || ''}</cbc:Name>
            </cac:PartyName>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>30</cbc:PaymentMeansCode>
        <cbc:PaymentDueDate>${dueDate}</cbc:PaymentDueDate>
        <cac:PayeeFinancialAccount>
            <cbc:ID>${bankAccount}</cbc:ID>
            <cac:FinancialInstitutionBranch>
                <cbc:ID>${branchCode}</cbc:ID>
            </cac:FinancialInstitutionBranch>
        </cac:PayeeFinancialAccount>
    </cac:PaymentMeans>
    <cac:PaymentTerms>
        <cbc:Note>${paymentTerms}</cbc:Note>
    </cac:PaymentTerms>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="${currency}">${tax.toFixed(2)}</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="${currency}">${subtotal.toFixed(2)}</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="${currency}">${tax.toFixed(2)}</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>${taxRate}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>${taxScheme}</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="${currency}">${subtotal.toFixed(2)}</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="${currency}">${subtotal.toFixed(2)}</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="${currency}">${total.toFixed(2)}</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="${currency}">${total.toFixed(2)}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:InvoicedQuantity unitCode="EA">${qty}</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="${currency}">${subtotal.toFixed(2)}</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Description>Supply of goods from ${formatted?.supplier || 'Supplier'} - Order ${formatted?.orderRef || id}</cbc:Description>
            <cbc:Name>Order ${formatted?.orderRef || id}</cbc:Name>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="${currency}">${parseFloat(unitPrice).toFixed(2)}</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
</Invoice>`

        setGeneratedXml(xml)
        setStep(3)
    }

    const handleSave = async () => {
        setSaving(true)
        setSaveError('')
        const token = localStorage.getItem('accessToken')
        console.log('token:', token)
        try {
            const response = await fetch(`${API}/api/invoice/invoice`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({
                    invoiceId: invoiceNumber,
                    xml: generatedXml,
                    metadata: {
                        invoice_id: invoiceNumber,
                        order_ref: formatted?.orderRef || '',
                        despatch_ref: id,
                        customer: formatted?.customer || '',
                        supplier: formatted?.supplier || '',
                        issue_date: issueDate,
                        due_date: dueDate,
                        currency,
                        total: total.toFixed(2),
                        standard: standard?.standard || '',
                        status: 'Unpaid'
                    }
                })
            })
            console.log('status:', response.status)
            const text = await response.text()
            console.log('response body:', text)
            if (response.ok) {
                navigate('/invoices')
            } else {
                setSaveError('Failed to save invoice. Please try again.')
            }
        } catch (e) {
            console.log('error:', e)
            setSaveError('Failed to save invoice. Please try again.')
        } finally {
            setSaving(false)
        }
    }

    const downloadXml = () => {
        const blob = new Blob([generatedXml], { type: 'application/xml' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${invoiceNumber}.xml`
        a.click()
        URL.revokeObjectURL(url)
    }

    return (
        <SellerDashboardLayout>
            <div className="mb-8">
                <button onClick={() => navigate(`/despatch/${id}`)} className="text-gray-500 hover:text-gray-700 text-sm mb-2 block">← Back</button>
                <h1 className="text-2xl font-bold">Generate Invoice</h1>
            </div>

            {/* Stepper */}
            <div className="flex items-center gap-2 mb-8">
                {['Select Standard', 'Invoice Details', 'Review & Submit'].map((label, index) => (
                    <div key={index} className="flex items-center gap-2">
                        <div className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-medium ${stepClass(index)}`}>
                            {step > index + 1 ? '✓' : index + 1}
                        </div>
                        <span className={`text-sm ${step === index + 1 ? 'text-deep-sky-blue-600 font-medium' : 'text-gray-400'}`}>{label}</span>
                        {index < 2 && <div className="w-12 h-px bg-gray-200 mx-1" />}
                    </div>
                ))}
            </div>

            {loading ? (
                <p className="text-gray-400">Loading despatch advice...</p>
            ) : (
                <>
                    {/* Step 1 - Select Standard */}
                    {step === 1 && (
                        <div className="max-w-2xl">
                            <p className="text-gray-500 mb-4">Select the e-invoicing standard for the destination country.</p>
                            <div className="flex flex-col gap-3">
                                {STANDARDS.map((s) => (
                                    <button
                                        key={s.code}
                                        onClick={() => setSelectedStandard(s.code)}
                                        className={`text-left p-4 rounded-xl border-2 transition-colors ${selectedStandard === s.code ? 'border-deep-sky-blue-600 bg-deep-sky-blue-50' : 'border-gray-200 hover:border-gray-300 bg-white'}`}
                                    >
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="font-medium text-gray-800">{s.label}</p>
                                                <p className="text-sm text-deep-sky-blue-600">{s.standard}</p>
                                                <p className="text-xs text-gray-400 mt-1">{s.description}</p>
                                            </div>
                                            {selectedStandard === s.code && (
                                                <div className="w-6 h-6 rounded-full bg-deep-sky-blue-600 flex items-center justify-center text-white text-xs flex-shrink-0 ml-4">✓</div>
                                            )}
                                        </div>
                                    </button>
                                ))}
                            </div>
                            <div className="flex justify-end mt-6">
                                <button
                                    onClick={() => setStep(2)}
                                    disabled={!selectedStandard}
                                    className="bg-deep-sky-blue-600 text-white px-6 py-2 rounded-lg hover:bg-deep-sky-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Next →
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Step 2 - Invoice Details */}
                    {step === 2 && (
                        <div className="max-w-2xl flex flex-col gap-6">
                            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                                <h2 className="text-lg font-semibold mb-4">Invoice Details</h2>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">Invoice Number</label>
                                        <input type="text" value={invoiceNumber} onChange={(e) => setInvoiceNumber(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">Payment Terms</label>
                                        <select value={paymentTerms} onChange={(e) => setPaymentTerms(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm">
                                            <option value="Net 7">Net 7</option>
                                            <option value="Net 14">Net 14</option>
                                            <option value="Net 30">Net 30</option>
                                            <option value="Net 60">Net 60</option>
                                            <option value="Due on receipt">Due on receipt</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">Issue Date</label>
                                        <input type="date" value={issueDate} onChange={(e) => setIssueDate(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">Due Date</label>
                                        <input type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">Unit Price ({currency})</label>
                                        <input type="number" placeholder="0.00" value={unitPrice} onChange={(e) => setUnitPrice(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">{taxScheme} Rate (%)</label>
                                        <input type="number" value={taxRate} onChange={(e) => setTaxRate(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                    <div className="col-span-2">
                                        <label className="text-sm text-gray-600 mb-1 block">Note (optional)</label>
                                        <input type="text" placeholder="Any additional notes..." value={note} onChange={(e) => setNote(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                </div>
                            </div>

                            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                                <h2 className="text-lg font-semibold mb-4">Payment Details</h2>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">{paymentLabels.account}</label>
                                        <input type="text" placeholder="e.g. 123456789" value={bankAccount} onChange={(e) => setBankAccount(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                    <div>
                                        <label className="text-sm text-gray-600 mb-1 block">{paymentLabels.branch}</label>
                                        <input type="text" placeholder={selectedStandard === 'AU' ? 'e.g. 062-000' : selectedStandard === 'EU' ? 'e.g. DEUTDEDB' : 'e.g. 021000021'} value={branchCode} onChange={(e) => setBranchCode(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    </div>
                                </div>
                            </div>

                            <div className="flex justify-between">
                                <button onClick={() => setStep(1)} className="border border-gray-300 text-gray-600 px-6 py-2 rounded-lg hover:bg-gray-50">← Back</button>
                                <button
                                    onClick={handleGenerate}
                                    disabled={!canGenerate}
                                    className="bg-deep-sky-blue-600 text-white px-6 py-2 rounded-lg hover:bg-deep-sky-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Generate Invoice →
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Step 3 - Review & Submit */}
                    {step === 3 && (
                        <div className="max-w-2xl flex flex-col gap-6">
                            <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-center gap-3">
                                <span className="text-green-600 text-xl">✓</span>
                                <div>
                                    <p className="font-medium text-green-700">Invoice Generated</p>
                                    <p className="text-sm text-green-600">{invoiceNumber} · {standard?.standard} · {currency} {total.toFixed(2)}</p>
                                </div>
                            </div>

                            {saveError && (
                                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center justify-between">
                                    <p className="text-sm text-red-600">{saveError}</p>
                                    <button onClick={() => setSaveError('')} className="text-red-400 hover:text-red-600 font-bold text-lg leading-none">✕</button>
                                </div>
                            )}

                            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                                <div className="flex justify-between items-center mb-4">
                                    <h2 className="text-lg font-semibold">Invoice Document</h2>
                                    <div className="flex gap-3">
                                        <button onClick={() => setShowRaw(!showRaw)} className="text-sm border border-gray-300 px-4 py-1 rounded-md hover:bg-gray-50">
                                            {showRaw ? 'View Formatted' : 'View Raw XML'}
                                        </button>
                                        <button onClick={downloadXml} className="border border-gray-300 text-gray-600 text-sm px-4 py-1 rounded-md hover:bg-gray-50">
                                            Download XML
                                        </button>
                                    </div>
                                </div>
                                {showRaw ? (
                                    <pre className="bg-gray-50 border border-gray-100 rounded-lg p-4 text-sm overflow-auto max-h-96">
                                        {generatedXml}
                                    </pre>
                                ) : (
                                    <div className="bg-gray-50 border border-gray-100 rounded-lg p-4 text-sm flex flex-col gap-2">
                                        <p><span className="text-gray-500 font-medium">Invoice Number:</span> {invoiceNumber}</p>
                                        <p><span className="text-gray-500 font-medium">Standard:</span> {standard?.standard}</p>
                                        <p><span className="text-gray-500 font-medium">Issue Date:</span> {issueDate}</p>
                                        <p><span className="text-gray-500 font-medium">Due Date:</span> {dueDate}</p>
                                        <p><span className="text-gray-500 font-medium">Supplier:</span> {formatted?.supplier}</p>
                                        <p><span className="text-gray-500 font-medium">Customer:</span> {formatted?.customer}</p>
                                        <p><span className="text-gray-500 font-medium">Order Reference:</span> {formatted?.orderRef}</p>
                                        <p><span className="text-gray-500 font-medium">Despatch Reference:</span> {id}</p>
                                        <p><span className="text-gray-500 font-medium">Quantity:</span> {qty}</p>
                                        <p><span className="text-gray-500 font-medium">Unit Price:</span> {currency} {parseFloat(unitPrice).toFixed(2)}</p>
                                        <p><span className="text-gray-500 font-medium">Subtotal:</span> {currency} {subtotal.toFixed(2)}</p>
                                        <p><span className="text-gray-500 font-medium">{taxScheme} ({taxRate}%):</span> {currency} {tax.toFixed(2)}</p>
                                        <p><span className="text-gray-500 font-medium">Total:</span> {currency} {total.toFixed(2)}</p>
                                        <p><span className="text-gray-500 font-medium">Payment Terms:</span> {paymentTerms}</p>
                                        {bankAccount && <p><span className="text-gray-500 font-medium">{paymentLabels.account}:</span> {bankAccount}</p>}
                                        {branchCode && <p><span className="text-gray-500 font-medium">{paymentLabels.branch}:</span> {branchCode}</p>}
                                        {note && <p><span className="text-gray-500 font-medium">Note:</span> {note}</p>}
                                    </div>
                                )}
                            </div>

                            <div className="flex justify-between">
                                <button onClick={() => setStep(2)} className="border border-gray-300 text-gray-600 px-6 py-2 rounded-lg hover:bg-gray-50">← Back</button>
                                <button
                                    onClick={handleSave}
                                    disabled={saving}
                                    className="bg-deep-sky-blue-600 text-white px-6 py-2 rounded-lg hover:bg-deep-sky-blue-700 disabled:opacity-50"
                                >
                                    {saving ? 'Saving...' : 'Save & Done'}
                                </button>
                            </div>
                        </div>
                    )}
                </>
            )}
        </SellerDashboardLayout>
    )
}