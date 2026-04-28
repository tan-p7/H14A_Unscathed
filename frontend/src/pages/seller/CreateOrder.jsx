import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

const API = import.meta.env.VITE_API_URL ?? '/atlas'

const EMPTY_LINE = { itemName: '', description: '', quantity: '1', unitCode: 'EA', unitPrice: '' }

export default function CreateOrder() {
    const navigate = useNavigate()
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')

    // Order details
    const year = new Date().getFullYear()
    const seq = String(Math.floor(Math.random() * 9000) + 1000)
    const [orderId] = useState(`PO-${year}-${seq}`)
    const [issueDate, setIssueDate] = useState(new Date().toISOString().split('T')[0])
    const [currency, setCurrency] = useState('AUD')
    const [paymentMeans, setPaymentMeans] = useState('30')
    const [note, setNote] = useState('')
    const [requestedDeliveryDate, setRequestedDeliveryDate] = useState('')

    // Buyer
    const [buyerName, setBuyerName] = useState('')
    const [buyerStreet, setBuyerStreet] = useState('')
    const [buyerCity, setBuyerCity] = useState('')
    const [buyerPostal, setBuyerPostal] = useState('')
    const [buyerState, setBuyerState] = useState('')
    const [buyerCountry, setBuyerCountry] = useState('AU')
    const [buyerTaxId, setBuyerTaxId] = useState('')

    // Seller
    const [sellerName, setSellerName] = useState('')
    const [sellerStreet, setSellerStreet] = useState('')
    const [sellerCity, setSellerCity] = useState('')
    const [sellerPostal, setSellerPostal] = useState('')
    const [sellerState, setSellerState] = useState('')
    const [sellerCountry, setSellerCountry] = useState('AU')
    const [sellerTaxId, setSellerTaxId] = useState('')

    // Line items
    const [lines, setLines] = useState([{ ...EMPTY_LINE }])

    const updateLine = (index, field, value) => {
        setLines(prev => prev.map((l, i) => i === index ? { ...l, [field]: value } : l))
    }
    const addLine = () => setLines(prev => [...prev, { ...EMPTY_LINE }])
    const removeLine = (index) => setLines(prev => prev.filter((_, i) => i !== index))

    const subtotal = lines.reduce((sum, l) => sum + (parseFloat(l.quantity) || 0) * (parseFloat(l.unitPrice) || 0), 0)

    const canSubmit = orderId && issueDate && buyerName && sellerName && lines.every(l => l.itemName && l.quantity && l.unitPrice)

    const handleSave = async () => {
        setSaving(true)
        setError('')

        const xml = `<?xml version="1.0" encoding="UTF-8"?>
<Order xmlns="urn:oasis:names:specification:ubl:schema:xsd:Order-2"
    xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
    xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2">
    <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
    <cbc:ID>${orderId}</cbc:ID>
    <cbc:IssueDate>${issueDate}</cbc:IssueDate>
    <cbc:DocumentCurrencyCode>${currency}</cbc:DocumentCurrencyCode>
    ${note ? `<cbc:Note>${note}</cbc:Note>` : ''}
    <cac:OrderReference>
        <cbc:ID>${orderId}</cbc:ID>
        <cbc:IssueDate>${issueDate}</cbc:IssueDate>
    </cac:OrderReference>
    <cac:BuyerCustomerParty>
        <cac:Party>
            <cac:PartyName><cbc:Name>${buyerName}</cbc:Name></cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>${buyerStreet}</cbc:StreetName>
                <cbc:CityName>${buyerCity}</cbc:CityName>
                <cbc:PostalZone>${buyerPostal}</cbc:PostalZone>
                <cbc:CountrySubentity>${buyerState}</cbc:CountrySubentity>
                <cac:Country><cbc:IdentificationCode>${buyerCountry}</cbc:IdentificationCode></cac:Country>
            </cac:PostalAddress>
            ${buyerTaxId ? `<cac:PartyTaxScheme><cbc:CompanyID>${buyerTaxId}</cbc:CompanyID><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:PartyTaxScheme>` : ''}
        </cac:Party>
    </cac:BuyerCustomerParty>
    <cac:SellerSupplierParty>
        <cac:Party>
            <cac:PartyName><cbc:Name>${sellerName}</cbc:Name></cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>${sellerStreet}</cbc:StreetName>
                <cbc:CityName>${sellerCity}</cbc:CityName>
                <cbc:PostalZone>${sellerPostal}</cbc:PostalZone>
                <cbc:CountrySubentity>${sellerState}</cbc:CountrySubentity>
                <cac:Country><cbc:IdentificationCode>${sellerCountry}</cbc:IdentificationCode></cac:Country>
            </cac:PostalAddress>
            ${sellerTaxId ? `<cac:PartyTaxScheme><cbc:CompanyID>${sellerTaxId}</cbc:CompanyID><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:PartyTaxScheme>` : ''}
        </cac:Party>
    </cac:SellerSupplierParty>
    <cac:Delivery>
        ${requestedDeliveryDate ? `<cac:RequestedDeliveryPeriod><cbc:EndDate>${requestedDeliveryDate}</cbc:EndDate></cac:RequestedDeliveryPeriod>` : ''}
        <cac:DeliveryAddress>
            <cbc:StreetName>${buyerStreet}</cbc:StreetName>
            <cbc:CityName>${buyerCity}</cbc:CityName>
            <cbc:PostalZone>${buyerPostal}</cbc:PostalZone>
            <cac:Country><cbc:IdentificationCode>${buyerCountry}</cbc:IdentificationCode></cac:Country>
        </cac:DeliveryAddress>
    </cac:Delivery>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>${paymentMeans}</cbc:PaymentMeansCode>
    </cac:PaymentMeans>
    ${lines.map((l, i) => `
    <cac:OrderLine>
        <cac:LineItem>
            <cbc:ID>${i + 1}</cbc:ID>
            <cbc:Quantity unitCode="${l.unitCode}">${l.quantity}</cbc:Quantity>
            <cbc:LineExtensionAmount currencyID="${currency}">${((parseFloat(l.quantity) || 0) * (parseFloat(l.unitPrice) || 0)).toFixed(2)}</cbc:LineExtensionAmount>
            <cac:Price>
                <cbc:PriceAmount currencyID="${currency}">${parseFloat(l.unitPrice || 0).toFixed(2)}</cbc:PriceAmount>
            </cac:Price>
            <cac:Item>
                <cbc:Description>${l.description}</cbc:Description>
                <cbc:Name>${l.itemName}</cbc:Name>
            </cac:Item>
        </cac:LineItem>
    </cac:OrderLine>`).join('')}
</Order>`

        const token = localStorage.getItem('accessToken')
        try {
            const response = await fetch(`${API}/api/order/order`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({
                    orderId,
                    xml,
                    metadata: {
                        order_id: orderId,
                        buyer: buyerName,
                        seller: sellerName,
                        issue_date: issueDate,
                        currency,
                        total: subtotal.toFixed(2),
                        status: 'Pending',
                        line_count: lines.length
                    }
                })
            })
            if (response.ok) {
                navigate('/orders')
            } else {
                const text = await response.text()
                setError(`Failed to save order: ${text}`)
            }
        } catch (e) {
            setError('Failed to save order. Please try again.')
        } finally {
            setSaving(false)
        }
    }

    const countryOptions = [
        ['AU', 'Australia'], ['NZ', 'New Zealand'], ['US', 'United States'],
        ['GB', 'United Kingdom'], ['CA', 'Canada'], ['SG', 'Singapore'],
        ['JP', 'Japan'], ['CN', 'China'], ['IN', 'India'],
        ['DE', 'Germany'], ['FR', 'France']
    ]

    return (
        <SellerDashboardLayout>
            <div className="mb-6">
                <button onClick={() => navigate('/orders')} className="text-gray-500 hover:text-gray-700 text-sm mb-2 block">← Back</button>
                <h1 className="text-2xl font-bold">Create Purchase Order</h1>
            </div>

            {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center justify-between mb-6 max-w-4xl">
                    <p className="text-sm text-red-600">{error}</p>
                    <button onClick={() => setError('')} className="text-red-400 hover:text-red-600 font-bold text-lg leading-none">✕</button>
                </div>
            )}

            <div className="max-w-4xl flex flex-col gap-6">

                {/* Order Details */}
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Order Details</h2>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="text-sm text-gray-600 mb-1 block">Order ID</label>
                            <input type="text" value={orderId} readOnly className="w-full border border-gray-200 bg-gray-50 rounded-lg px-4 py-2 text-sm text-gray-500" />
                        </div>
                        <div>
                            <label className="text-sm text-gray-600 mb-1 block">Issue Date</label>
                            <input type="date" value={issueDate} onChange={(e) => setIssueDate(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                        </div>
                        <div>
                            <label className="text-sm text-gray-600 mb-1 block">Currency</label>
                            <select value={currency} onChange={(e) => setCurrency(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm">
                                <option value="AUD">AUD</option>
                                <option value="USD">USD</option>
                                <option value="EUR">EUR</option>
                                <option value="GBP">GBP</option>
                                <option value="SGD">SGD</option>
                                <option value="JPY">JPY</option>
                            </select>
                        </div>
                        <div>
                            <label className="text-sm text-gray-600 mb-1 block">Payment Means</label>
                            <select value={paymentMeans} onChange={(e) => setPaymentMeans(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm">
                                <option value="30">Bank Transfer (30)</option>
                                <option value="42">Payment to Bank Account (42)</option>
                                <option value="48">Bank Card (48)</option>
                                <option value="49">Direct Debit (49)</option>
                                <option value="97">Clearing Between Partners (97)</option>
                            </select>
                        </div>
                        <div>
                            <label className="text-sm text-gray-600 mb-1 block">Requested Delivery Date</label>
                            <input type="date" value={requestedDeliveryDate} onChange={(e) => setRequestedDeliveryDate(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                        </div>
                        <div>
                            <label className="text-sm text-gray-600 mb-1 block">Note (optional)</label>
                            <input type="text" value={note} onChange={(e) => setNote(e.target.value)} placeholder="Any additional notes..." className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                        </div>
                    </div>
                </div>

                {/* Buyer & Seller */}
                <div className="grid grid-cols-2 gap-6">
                    {/* Buyer */}
                    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                        <h2 className="text-lg font-semibold mb-4">Buyer Details</h2>
                        <div className="flex flex-col gap-3">
                            <div>
                                <label className="text-sm text-gray-600 mb-1 block">Company Name *</label>
                                <input type="text" value={buyerName} onChange={(e) => setBuyerName(e.target.value)} placeholder="e.g. Acme Corp" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                            </div>
                            <div>
                                <label className="text-sm text-gray-600 mb-1 block">Tax ID (ABN/GST)</label>
                                <input type="text" value={buyerTaxId} onChange={(e) => setBuyerTaxId(e.target.value)} placeholder="e.g. 51 824 753 556" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                            </div>
                            <div>
                                <label className="text-sm text-gray-600 mb-1 block">Street</label>
                                <input type="text" value={buyerStreet} onChange={(e) => setBuyerStreet(e.target.value)} placeholder="e.g. 123 Main St" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">City</label>
                                    <input type="text" value={buyerCity} onChange={(e) => setBuyerCity(e.target.value)} placeholder="Sydney" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">Postal</label>
                                    <input type="text" value={buyerPostal} onChange={(e) => setBuyerPostal(e.target.value)} placeholder="2000" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">State</label>
                                    <input type="text" value={buyerState} onChange={(e) => setBuyerState(e.target.value)} placeholder="NSW" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">Country</label>
                                    <select value={buyerCountry} onChange={(e) => setBuyerCountry(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm">
                                        {countryOptions.map(([code, label]) => <option key={code} value={code}>{label}</option>)}
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Seller */}
                    <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                        <h2 className="text-lg font-semibold mb-4">Seller Details</h2>
                        <div className="flex flex-col gap-3">
                            <div>
                                <label className="text-sm text-gray-600 mb-1 block">Company Name *</label>
                                <input type="text" value={sellerName} onChange={(e) => setSellerName(e.target.value)} placeholder="e.g. Atlas Supply Co" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                            </div>
                            <div>
                                <label className="text-sm text-gray-600 mb-1 block">Tax ID (ABN/GST)</label>
                                <input type="text" value={sellerTaxId} onChange={(e) => setSellerTaxId(e.target.value)} placeholder="e.g. 51 824 753 556" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                            </div>
                            <div>
                                <label className="text-sm text-gray-600 mb-1 block">Street</label>
                                <input type="text" value={sellerStreet} onChange={(e) => setSellerStreet(e.target.value)} placeholder="e.g. 456 Trade Ave" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">City</label>
                                    <input type="text" value={sellerCity} onChange={(e) => setSellerCity(e.target.value)} placeholder="Melbourne" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">Postal</label>
                                    <input type="text" value={sellerPostal} onChange={(e) => setSellerPostal(e.target.value)} placeholder="3000" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">State</label>
                                    <input type="text" value={sellerState} onChange={(e) => setSellerState(e.target.value)} placeholder="VIC" className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                                <div>
                                    <label className="text-sm text-gray-600 mb-1 block">Country</label>
                                    <select value={sellerCountry} onChange={(e) => setSellerCountry(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm">
                                        {countryOptions.map(([code, label]) => <option key={code} value={code}>{label}</option>)}
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Line Items */}
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-lg font-semibold">Line Items</h2>
                        <button onClick={addLine} className="text-sm text-deep-sky-blue-600 border border-deep-sky-blue-300 px-3 py-1.5 rounded-lg hover:bg-deep-sky-blue-50">
                            + Add Item
                        </button>
                    </div>
                    <div className="flex flex-col gap-3">
                        {lines.map((line, index) => (
                            <div key={index} className="grid grid-cols-12 gap-2 items-end">
                                <div className="col-span-3">
                                    {index === 0 && <label className="text-xs text-gray-500 mb-1 block">Item Name *</label>}
                                    <input type="text" value={line.itemName} onChange={(e) => updateLine(index, 'itemName', e.target.value)} placeholder="e.g. Widget A" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                                </div>
                                <div className="col-span-3">
                                    {index === 0 && <label className="text-xs text-gray-500 mb-1 block">Description</label>}
                                    <input type="text" value={line.description} onChange={(e) => updateLine(index, 'description', e.target.value)} placeholder="Description" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                                </div>
                                <div className="col-span-2">
                                    {index === 0 && <label className="text-xs text-gray-500 mb-1 block">Qty *</label>}
                                    <input type="number" value={line.quantity} onChange={(e) => updateLine(index, 'quantity', e.target.value)} placeholder="1" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                                </div>
                                <div className="col-span-1">
                                    {index === 0 && <label className="text-xs text-gray-500 mb-1 block">Unit</label>}
                                    <select value={line.unitCode} onChange={(e) => updateLine(index, 'unitCode', e.target.value)} className="w-full border border-gray-300 rounded-lg px-2 py-2 text-sm">
                                        <option value="EA">EA</option>
                                        <option value="KG">KG</option>
                                        <option value="LTR">LTR</option>
                                        <option value="MTR">MTR</option>
                                        <option value="BOX">BOX</option>
                                    </select>
                                </div>
                                <div className="col-span-2">
                                    {index === 0 && <label className="text-xs text-gray-500 mb-1 block">Unit Price *</label>}
                                    <input type="number" value={line.unitPrice} onChange={(e) => updateLine(index, 'unitPrice', e.target.value)} placeholder="0.00" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                                </div>
                                <div className="col-span-1 flex justify-end">
                                    {lines.length > 1 && (
                                        <button onClick={() => removeLine(index)} className="text-red-400 hover:text-red-600 text-lg leading-none pb-2">✕</button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="mt-4 pt-4 border-t border-gray-100 flex justify-end">
                        <div className="text-right">
                            <p className="text-sm text-gray-500">Subtotal</p>
                            <p className="text-xl font-bold text-gray-900">{currency} {subtotal.toFixed(2)}</p>
                        </div>
                    </div>
                </div>

                <div className="flex justify-end">
                    <button
                        onClick={handleSave}
                        disabled={!canSubmit || saving}
                        className="bg-deep-sky-blue-600 text-white px-6 py-3 rounded-lg hover:bg-deep-sky-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {saving ? 'Saving...' : 'Create Order'}
                    </button>
                </div>
            </div>
        </SellerDashboardLayout>
    )
}