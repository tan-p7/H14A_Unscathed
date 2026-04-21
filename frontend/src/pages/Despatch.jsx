import { useState } from "react";
import { Link } from "react-router-dom";
import DashboardLayout from "../components/DashboardLayout";

const fakeDespatch = [
    { id: 'DA-2025-001', orderId: 'PO-2026-001', date: '2026-04-01', status: 'Pending' },
    { id: 'DA-2026-002', orderId: 'PO-2026-002', date: '2026-04-05', status: 'Shipped' },
    { id: 'DA-2026-003', orderId: 'PO-2026-003', date: '2026-04-10', status: 'Delivered' },
]

export default function Despatch() {
    const [search, setSearch] = useState('')
    const [filter, setFilter] = useState('All')

    const filteredDespatch = fakeDespatch
        .filter(d => filter === 'All' || d.status === filter)
        .filter(d => d.id.toLowerCase().includes(search.toLowerCase()) || d.orderId.toLowerCase().includes(search.toLowerCase()))

    return (
        <DashboardLayout>
            <div className="flex flex-col h-full">
                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-2xl font-bold">Despatch Advice</h1>
                    <Link to="/create-despatch">
                        <button className="bg-deep-sky-blue-600 text-white px-4 py-2 rounded-lg hover:bg-deep-sky-blue-700">
                            + Create Despatch
                        </button>
                    </Link>
                </div>

                <div className="flex gap-4 mb-4">
                    <input
                        type="text"
                        placeholder="Search despatch..."
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                        className="border border-gray-300 rounded-lg px-4 py-2 w-64"
                    />
                    <div className="flex gap-2">
                        {['All', 'Pending', 'Shipped', 'Delivered'].map((status) => (
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
                                <th className="px-4 py-3 border-b border-gray-100">Despatch ID</th>
                                <th className="px-4 py-3 border-b border-gray-100">Order ID</th>
                                <th className="px-4 py-3 border-b border-gray-100">Date</th>
                                <th className="px-4 py-3 border-b border-gray-100">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredDespatch.map((d, index) => (
                                <tr key={index} className="hover:bg-gray-50 border-b border-gray-100">
                                    <td className="px-4 py-3 text-deep-sky-blue-600">{d.id}</td>
                                    <td className="px-4 py-3">{d.orderId}</td>
                                    <td className="px-4 py-3 text-gray-500">{d.date}</td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                            d.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                                            d.status === 'Shipped' ? 'bg-blue-100 text-blue-700' :
                                            d.status === 'Delivered' ? 'bg-green-100 text-green-700' :
                                            'bg-gray-100 text-gray-600'
                                        }`}>
                                            {d.status}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </DashboardLayout>
    )
}