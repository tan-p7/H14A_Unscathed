import { useState } from 'react'
import CustomerDashboardLayout from '../../components/customer/CustomerDashboardLayout'

const fakeDeliveries = [
    { id: 'DA-260420-00001', orderId: 'PO-2026-007', date: '2026-04-21', expectedDelivery: '2026-04-23', status: 'In Transit', supplier: 'Atlas Supplies' },
    { id: 'DA-260418-00003', orderId: 'PO-2026-005', date: '2026-04-19', expectedDelivery: '2026-04-21', status: 'Out for Delivery', supplier: 'Global Traders' },
    { id: 'DA-260415-00002', orderId: 'PO-2026-003', date: '2026-04-16', expectedDelivery: '2026-04-18', status: 'Delivered', supplier: 'Atlas Supplies' },
    { id: 'DA-260410-00001', orderId: 'PO-2026-001', date: '2026-04-11', expectedDelivery: '2026-04-13', status: 'Delivered', supplier: 'Global Traders' },
]

export default function CustomerDespatch() {
    const [search, setSearch] = useState('')
    const [filter, setFilter] = useState('All')

    const filtered = fakeDeliveries
        .filter(d => filter === 'All' || d.status === filter)
        .filter(d => d.id.toLowerCase().includes(search.toLowerCase()) || d.orderId.toLowerCase().includes(search.toLowerCase()))

    return (
        <CustomerDashboardLayout>
            <div className="flex flex-col h-full">
                <h1 className="text-2xl font-bold mb-4">My Deliveries</h1>
                <div className="flex gap-4 mb-4">
                    <input type="text" placeholder="Search deliveries..." value={search} onChange={(e) => setSearch(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 w-64" />
                    <div className="flex gap-2">
                        {['All', 'In Transit', 'Out for Delivery', 'Delivered'].map((status) => (
                            <button key={status} onClick={() => setFilter(status)} className={`px-4 py-2 rounded-md text-sm ${filter === status ? 'bg-deep-sky-blue-600 text-white' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'}`}>{status}</button>
                        ))}
                    </div>
                </div>
                <div className="rounded-xl shadow-sm border border-gray-300 overflow-hidden flex-1 overflow-y-auto">
                    <table className="w-full border-collapse">
                        <thead className="sticky top-0 bg-gray-200">
                            <tr className="text-left text-gray-600 text-sm">
                                <th className="px-4 py-3 border-b border-gray-300">Despatch ID</th>
                                <th className="px-4 py-3 border-b border-gray-300">Order ID</th>
                                <th className="px-4 py-3 border-b border-gray-300">Supplier</th>
                                <th className="px-4 py-3 border-b border-gray-300">Dispatched</th>
                                <th className="px-4 py-3 border-b border-gray-300">Expected</th>
                                <th className="px-4 py-3 border-b border-gray-300">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filtered.length === 0 ? (
                                <tr><td colSpan="6" className="px-4 py-8 text-center text-gray-400">No deliveries found.</td></tr>
                            ) : (
                                filtered.map((d, index) => (
                                    <tr key={index} className="hover:bg-gray-50 border-b border-gray-200">
                                        <td className="px-4 py-3 text-deep-sky-blue-600 text-sm">{d.id}</td>
                                        <td className="px-4 py-3 text-sm">{d.orderId}</td>
                                        <td className="px-4 py-3 text-sm">{d.supplier}</td>
                                        <td className="px-4 py-3 text-gray-500 text-sm">{d.date}</td>
                                        <td className="px-4 py-3 text-gray-500 text-sm">{d.expectedDelivery}</td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                                d.status === 'Delivered' ? 'bg-green-100 text-green-700' :
                                                d.status === 'Out for Delivery' ? 'bg-blue-100 text-blue-700' :
                                                'bg-yellow-100 text-yellow-700'
                                            }`}>{d.status}</span>
                                        </td>
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