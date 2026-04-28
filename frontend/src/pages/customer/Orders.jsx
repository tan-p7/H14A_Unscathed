import { useState } from 'react'
import { Link } from 'react-router-dom'
import CustomerDashboardLayout from '../../components/customer/CustomerDashboardLayout'

const fakeOrders = [
    { id: 'PO-2026-008', seller: 'Atlas Supplies', date: '2026-04-20', status: 'Pending', total: '$540.00', items: 3 },
    { id: 'PO-2026-007', seller: 'Atlas Supplies', date: '2026-04-18', status: 'Processing', total: '$1,200.00', items: 5 },
    { id: 'PO-2026-005', seller: 'Global Traders', date: '2026-04-15', status: 'Delivered', total: '$320.00', items: 2 },
    { id: 'PO-2026-003', seller: 'Atlas Supplies', date: '2026-04-10', status: 'Delivered', total: '$780.00', items: 4 },
    { id: 'PO-2026-001', seller: 'Global Traders', date: '2026-04-01', status: 'Delivered', total: '$1,980.00', items: 8 },
]

export default function CustomerOrders() {
    const [search, setSearch] = useState('')
    const [filter, setFilter] = useState('All')

    const filteredOrders = fakeOrders
        .filter(order => filter === 'All' || order.status === filter)
        .filter(order => order.id.toLowerCase().includes(search.toLowerCase()) || order.seller.toLowerCase().includes(search.toLowerCase()))

    return (
        <CustomerDashboardLayout>
            <div className="flex flex-col h-full">
                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-2xl font-bold">My Orders</h1>
                    <Link to="/customer-create-order">
                        <button className="bg-deep-sky-blue-600 text-white px-4 py-2 rounded-lg hover:bg-deep-sky-blue-700">+ Place Order</button>
                    </Link>
                </div>
                <div className="flex gap-4 mb-4">
                    <input type="text" placeholder="Search orders..." value={search} onChange={(e) => setSearch(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 w-64" />
                    <div className="flex gap-2">
                        {['All', 'Pending', 'Processing', 'Delivered'].map((status) => (
                            <button key={status} onClick={() => setFilter(status)} className={`px-4 py-2 rounded-md text-sm ${filter === status ? 'bg-deep-sky-blue-600 text-white' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'}`}>{status}</button>
                        ))}
                    </div>
                </div>
                <div className="rounded-xl shadow-sm border border-gray-300 overflow-hidden flex-1 overflow-y-auto">
                    <table className="w-full border-collapse">
                        <thead className="sticky top-0 bg-gray-200">
                            <tr className="text-left text-gray-600 text-sm">
                                <th className="px-4 py-3 border-b border-gray-300">Order ID</th>
                                <th className="px-4 py-3 border-b border-gray-300">Seller</th>
                                <th className="px-4 py-3 border-b border-gray-300">Date</th>
                                <th className="px-4 py-3 border-b border-gray-300">Items</th>
                                <th className="px-4 py-3 border-b border-gray-300">Status</th>
                                <th className="px-4 py-3 border-b border-gray-300">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredOrders.length === 0 ? (
                                <tr><td colSpan="6" className="px-4 py-8 text-center text-gray-400">No orders found.</td></tr>
                            ) : (
                                filteredOrders.map((order, index) => (
                                    <tr key={index} className="hover:bg-gray-50 border-b border-gray-200">
                                        <td className="px-4 py-3 text-deep-sky-blue-600 text-sm">{order.id}</td>
                                        <td className="px-4 py-3 text-sm">{order.seller}</td>
                                        <td className="px-4 py-3 text-gray-500 text-sm">{order.date}</td>
                                        <td className="px-4 py-3 text-gray-500 text-sm">{order.items}</td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                                order.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                                                order.status === 'Processing' ? 'bg-blue-100 text-blue-700' :
                                                'bg-green-100 text-green-700'
                                            }`}>{order.status}</span>
                                        </td>
                                        <td className="px-4 py-3 text-sm">{order.total}</td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </CustomerDashboardLayout>
    )
}