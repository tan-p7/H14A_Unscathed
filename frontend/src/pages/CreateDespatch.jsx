import { useState, useEffect, useRef } from 'react'
import DashboardLayout from '../components/DashboardLayout'

export default function CreateDespatch() {
    const [docId, setDocId] = useState(crypto.randomUUID())
    const [issueDate, setIssueDate] = useState(new Date().toISOString().split('T')[0])
    const [issueTime, setIssueTime] = useState(new Date().toTimeString().split(' ')[0])
    const [docNote, setDocNote] = useState('')
    const [orderRefId, setOrderRefId] = useState('')
    const [supplierPartyName, setSupplierPartyName] = useState('')
    const [supplierEndpointId, setSupplierEndpointId] = useState('')
    const [supplierSchemeId, setSupplierSchemeId] = useState('')
    const [customerPartyName, setCustomerPartyName] = useState('')
    const [customerEndpointId, setCustomerEndpointId] = useState('')
    const [customerSchemeId, setCustomerSchemeId] = useState('')
    const [streetName, setStreetName] = useState('')
    const [cityName, setCityName] = useState('')
    const [postalZone, setPostalZone] = useState('')
    const [country, setCountry] = useState('')
    const [countryCode, setCountryCode] = useState('')
    const [mode, setMode] = useState(null)
    const [file, setFile] = useState(null)
    const [hoverSelect, setHoverSelect] = useState(false)
    const [hoverUpload, setHoverUpload] = useState(false)
    const [hoverManual, setHoverManual] = useState(false)
    const fileInputRef = useRef(null)

    useEffect(() => {
        if (mode === 'upload' && fileInputRef.current) {
            fileInputRef.current.click()
            setMode(null)
            setHoverUpload(false)
        }
    }, [mode])

    const handleSubmit = async () => {
        if (mode === 'upload' && !file) return

        const token = localStorage.getItem('accessToken')
        let body

        if (file) {
            const xmlText = await file.text()
            body = JSON.stringify({ xml: xmlText })
        } else if (mode === 'manual') {
            body = JSON.stringify({
                xml: {
                    xmlns: 'urn:oasis:names:specification:ubl:schema:xsd:Order-2',
                    ID: docId,
                    IssueDate: issueDate,
                    IssueTime: issueTime,
                    Note: docNote,
                    orderReference: { id: orderRefId },
                    despatchSupplierParty: {
                        party: {
                            endpointId: { value: supplierEndpointId, schemeId: supplierSchemeId },
                            partyName: { name: supplierPartyName }
                        }
                    },
                    deliveryCustomerParty: {
                        party: {
                            endpointId: { value: customerEndpointId, schemeId: customerSchemeId },
                            partyName: { name: customerPartyName }
                        }
                    },
                    shipment: {
                        id: '1',
                        delivery: {
                            deliveryAddress: {
                                streetName,
                                cityName,
                                postalZone,
                                countrySubentity: country,
                                country: { identificationCode: countryCode }
                            }
                        }
                    }
                }
            })
        }

        const response = await fetch('/atlas/api/despatch/despatch-advice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body
        })

        if (response.ok) {
            console.log('Despatch created successfully')
        } else {
            console.log('Error creating despatch')
        }
    }

    return (
        <DashboardLayout>
            <h1 className="text-2xl font-bold mb-8">Create Despatch Advice</h1>

            <div className="max-w-2xl flex flex-col gap-6">
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Order Source</h2>
                    <div className="flex gap-4">
                        <button
                            onClick={() => setMode('select')}
                            onMouseEnter={() => setHoverSelect(true)}
                            onMouseLeave={() => setHoverSelect(false)}
                            className={`flex-1 py-3 rounded-lg border text-sm font-medium transition-colors duration-100 ${mode === 'select' || hoverSelect ? 'bg-deep-sky-blue-600 text-white border-deep-sky-blue-600' : 'bg-white text-gray-600 border-gray-300'}`}
                        >
                            Select Order
                        </button>
                        <button
                            onClick={() => setMode('upload')}
                            onMouseEnter={() => setHoverUpload(true)}
                            onMouseLeave={() => setHoverUpload(false)}
                            className={`flex-1 py-3 rounded-lg border text-sm font-medium transition-colors duration-100 ${hoverUpload ? 'bg-deep-sky-blue-600 text-white border-deep-sky-blue-600' : 'bg-white text-gray-600 border-gray-300'}`}
                        >
                            Upload XML
                        </button>
                        <button
                            onClick={() => setMode('manual')}
                            onMouseEnter={() => setHoverManual(true)}
                            onMouseLeave={() => setHoverManual(false)}
                            className={`flex-1 py-3 rounded-lg border text-sm font-medium transition-colors duration-100 ${mode === 'manual' || hoverManual ? 'bg-deep-sky-blue-600 text-white border-deep-sky-blue-600' : 'bg-white text-gray-600 border-gray-300'}`}
                        >
                            Manual Input
                        </button>
                    </div>

                    {file && (
                        <p className="text-sm text-gray-500 mt-3">Selected: {file.name}</p>
                    )}

                    <input
                        type="file"
                        accept=".xml"
                        ref={fileInputRef}
                        onChange={(event) => {
                            setFile(event.target.files[0])
                            setHoverUpload(false)
                        }}
                        className="hidden"
                    />

                    {mode === 'manual' && (
                        <div className="mt-6 flex flex-col gap-6">
                            <div>
                                <h3 className="text-sm font-semibold text-gray-600 mb-3">Document Details</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <input type="text" placeholder="ID" value={docId} onChange={(e) => setDocId(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="date" value={issueDate} onChange={(e) => setIssueDate(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="time" value={issueTime} onChange={(e) => setIssueTime(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Note" value={docNote} onChange={(e) => setDocNote(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                            </div>

                            <div>
                                <h3 className="text-sm font-semibold text-gray-600 mb-3">Order Reference</h3>
                                <input type="text" placeholder="Order Reference ID" value={orderRefId} onChange={(e) => setOrderRefId(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                            </div>

                            <div>
                                <h3 className="text-sm font-semibold text-gray-600 mb-3">Supplier</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <input type="text" placeholder="Party Name" value={supplierPartyName} onChange={(e) => setSupplierPartyName(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Endpoint ID" value={supplierEndpointId} onChange={(e) => setSupplierEndpointId(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Scheme ID" value={supplierSchemeId} onChange={(e) => setSupplierSchemeId(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                            </div>

                            <div>
                                <h3 className="text-sm font-semibold text-gray-600 mb-3">Customer</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <input type="text" placeholder="Party Name" value={customerPartyName} onChange={(e) => setCustomerPartyName(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Endpoint ID" value={customerEndpointId} onChange={(e) => setCustomerEndpointId(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Scheme ID" value={customerSchemeId} onChange={(e) => setCustomerSchemeId(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                            </div>

                            <div>
                                <h3 className="text-sm font-semibold text-gray-600 mb-3">Delivery Address</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <input type="text" placeholder="Street Name" value={streetName} onChange={(e) => setStreetName(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="City" value={cityName} onChange={(e) => setCityName(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Postal Zone" value={postalZone} onChange={(e) => setPostalZone(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Country" value={country} onChange={(e) => setCountry(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    <input type="text" placeholder="Country Code (e.g. AU)" value={countryCode} onChange={(e) => setCountryCode(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                </div>
                            </div>
                        </div>
                    )}

                    {mode === 'select' && (
                        <div className="mt-6">
                            <p className="text-gray-400 text-sm">Order selection coming soon</p>
                        </div>
                    )}
                </div>

                <div className="flex justify-end">
                    <button
                        onClick={handleSubmit}
                        className="bg-deep-sky-blue-600 text-white px-6 py-3 rounded-lg hover:bg-deep-sky-blue-700"
                    >
                        Create Despatch
                    </button>
                </div>
            </div>
        </DashboardLayout>
    )
}