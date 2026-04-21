import { useState } from 'react'
import DashboardLayout from '../components/DashboardLayout'

export default function CreateOrder() {
    const [orderName, setOrderName] = useState('')
    const [sellerId, setSellerId] = useState('')
    const [documentCurrencyCode, setDocumentCurrencyCode] = useState('AUD')
    const [paymentMethodCode, setPaymentMethodCode] = useState('')
    const [destinationCountryCode, setDestinationCountryCode] = useState('AU')
    return (
        <DashboardLayout>
            <h1 className="text-2xl font-bold mb-8">Create Order</h1>
            <form className="max-w-2xl">
                <h2 className="text-lg font-semibold mb-4">Order Details</h2>
                <input
                    type="text"
                    placeholder="Order Name"
                    value={orderName}
                    onChange={(event) => setOrderName(event.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4"/>
                <input
                    type="text"
                    placeholder="Seller ID"
                    value={sellerId}
                    onChange={(event) => setSellerId(event.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4"/>
                <input
                    type="text"
                    placeholder="Currency Code (e.g. AUD)"
                    value={documentCurrencyCode}
                    onChange={(event) => setDocumentCurrencyCode(event.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4"
                />
                <input
                    type="text"
                    placeholder="Payment Method (e.g. CreditCard)"
                    value={paymentMethodCode}
                    onChange={(event) => setPaymentMethodCode(event.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4"
                />
                <input
                    type="text"
                    placeholder="Destination Country (e.g. AU)"
                    value={destinationCountryCode}
                    onChange={(event) => setDestinationCountryCode(event.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4"
                />
            </form>
        </DashboardLayout>
    )
    
}