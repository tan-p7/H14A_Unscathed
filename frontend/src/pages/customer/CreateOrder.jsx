import { useState } from 'react'
import CustomerDashboardLayout from '../../components/customer/CustomerDashboardLayout'

export default function CustomerCreateOrder() {
    const [orderLines, setOrderLines] = useState([{ itemName: '', quantity: '', price: '' }])
    const [seller, setSeller] = useState('')
    const [deliveryAddress, setDeliveryAddress] = useState('')
    const [city, setCity] = useState('')
    const [postalZone, setPostalZone] = useState('')
    const [country, setCountry] = useState('AU')
    const [paymentMethod, setPaymentMethod] = useState('CreditCard')
    const [note, setNote] = useState('')

    const addLine = () => setOrderLines([...orderLines, { itemName: '', quantity: '', price: '' }])
    const removeLine = (index) => setOrderLines(orderLines.filter((_, i) => i !== index))
    const updateLine = (index, field, value) => {
        const updated = [...orderLines]
        updated[index][field] = value
        setOrderLines(updated)
    }

    const total = orderLines.reduce((sum, line) => {
        const qty = parseFloat(line.quantity) || 0
        const price = parseFloat(line.price) || 0
        return sum + qty * price
    }, 0)

    return (
        <CustomerDashboardLayout>
            <h1 className="text-2xl font-bold mb-8">Place Order</h1>
            <div className="max-w-3xl flex flex-col gap-6">

                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Seller Details</h2>
                    <input type="text" placeholder="Seller Name or ID" value={seller} onChange={(e) => setSeller(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                </div>

                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Order Lines</h2>
                    <div className="flex flex-col gap-3">
                        {orderLines.map((line, index) => (
                            <div key={index} className="grid grid-cols-4 gap-3 items-center">
                                <input type="text" placeholder="Item Name" value={line.itemName} onChange={(e) => updateLine(index, 'itemName', e.target.value)} className="col-span-2 border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                <input type="number" placeholder="Qty" value={line.quantity} onChange={(e) => updateLine(index, 'quantity', e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                <div className="flex items-center gap-2">
                                    <input type="number" placeholder="Price" value={line.price} onChange={(e) => updateLine(index, 'price', e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                                    {orderLines.length > 1 && (
                                        <button onClick={() => removeLine(index)} className="text-red-400 hover:text-red-600 text-lg leading-none">✕</button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                    <button onClick={addLine} className="mt-3 text-deep-sky-blue-600 text-sm hover:underline">+ Add Line</button>
                    <div className="flex justify-end mt-4 pt-4 border-t border-gray-100">
                        <p className="text-sm font-semibold">Total: <span className="text-deep-sky-blue-600">${total.toFixed(2)}</span></p>
                    </div>
                </div>

                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Delivery Address</h2>
                    <div className="grid grid-cols-2 gap-4">
                        <input type="text" placeholder="Street Address" value={deliveryAddress} onChange={(e) => setDeliveryAddress(e.target.value)} className="col-span-2 border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                        <input type="text" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                        <input type="text" placeholder="Postal Code" value={postalZone} onChange={(e) => setPostalZone(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm" />
                        <select value={country} onChange={(e) => setCountry(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm">
                            <option value="AU">Australia</option>
                            <option value="NZ">New Zealand</option>
                            <option value="US">United States</option>
                            <option value="GB">United Kingdom</option>
                            <option value="SG">Singapore</option>
                        </select>
                        <select value={paymentMethod} onChange={(e) => setPaymentMethod(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 text-sm">
                            <option value="CreditCard">Credit Card</option>
                            <option value="BankTransfer">Bank Transfer</option>
                            <option value="PayPal">PayPal</option>
                        </select>
                    </div>
                </div>

                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Additional Notes</h2>
                    <textarea placeholder="Any special instructions..." value={note} onChange={(e) => setNote(e.target.value)} className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm h-24 resize-none" />
                </div>

                <div className="flex justify-end">
                    <button className="bg-deep-sky-blue-600 text-white px-8 py-3 rounded-lg hover:bg-deep-sky-blue-700 font-medium">
                        Place Order
                    </button>
                </div>
            </div>
        </CustomerDashboardLayout>
    )
}