import { useState } from 'react'
import { Link } from 'react-router-dom'
import DashboardLayout from '../components/DashboardLayout'

const fakeOrders = [
    { id: 'PO-2026-001', name: 'Purchase Order A', date: '2026-04-01', status: 'Pending', total: '$1,200.00' },
    { id: 'PO-2026-002', name: 'Purchase Order B', date: '2026-04-05', status: 'Delivered', total: '$3,450.00' },
    { id: 'PO-2026-003', name: 'Purchase Order C', date: '2026-04-10', status: 'Processing', total: '$780.00' },
    { id: 'PO-2026-004', name: 'Purchase Order D', date: '2026-04-11', status: 'Pending', total: '$900.00' },
    { id: 'PO-2026-005', name: 'Purchase Order E', date: '2026-04-12', status: 'Delivered', total: '$2,100.00' },
]

export default function Orders() {
    const [search, setSearch] = useState('')
    const [filter, setFilter] = useState('All')

    const filteredOrders = fakeOrders
        .filter(order => filter === 'All' || order.status === filter)
        .filter(order => order.name.toLowerCase().includes(search.toLowerCase()) || order.id.toLowerCase().includes(search.toLowerCase()))

    return (
        <DashboardLayout>
            <div className="flex flex-col h-full">
                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-2xl font-bold">Orders</h1>
                    <Link to="/create-order">
                        <button className="bg-deep-sky-blue-600 text-white px-4 py-2 rounded-lg hover:bg-deep-sky-blue-700">
                            + Create Order
                        </button>
                    </Link>
                </div>

                <div className="flex gap-4 mb-4">
                    <input
                        type="text"
                        placeholder="Search orders..."
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                        className="border border-gray-300 rounded-lg px-4 py-2 w-64"
                    />
                    <div className="flex gap-2">
                        {['All', 'Pending', 'Processing', 'Delivered'].map((status) => (
                            <button
                                key={status}
                                onClick={() => setFilter(status)}
                                className={`px-4 py-2 rounded-md text-sm ${filter === status ? 'bg-deep-sky-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                            >
                                {status}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="rounded-xl shadow-sm border border-gray-200 overflow-hidden flex-1 overflow-y-auto">
                    <table className="w-full border-collapse">
                        <thead className="sticky top-0 bg-gray-50">
                            <tr className="text-left text-gray-500 text-sm">
                                <th className="px-4 py-3 border-b border-gray-100">Order ID</th>
                                <th className="px-4 py-3 border-b border-gray-100">Name</th>
                                <th className="px-4 py-3 border-b border-gray-100">Date</th>
                                <th className="px-4 py-3 border-b border-gray-100">Status</th>
                                <th className="px-4 py-3 border-b border-gray-100">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredOrders.map((order, index) => (
                                <tr key={index} className="hover:bg-gray-50 border-b border-gray-100">
                                    <td className="px-4 py-3 text-deep-sky-blue-600">{order.id}</td>
                                    <td className="px-4 py-3">{order.name}</td>
                                    <td className="px-4 py-3 text-gray-500">{order.date}</td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                            order.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                                            order.status === 'Delivered' ? 'bg-green-100 text-green-700' :
                                            order.status === 'Processing' ? 'bg-blue-100 text-blue-700' :
                                            'bg-gray-100 text-gray-600'
                                        }`}>
                                            {order.status}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3">{order.total}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </DashboardLayout>
    )
}