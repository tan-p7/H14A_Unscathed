import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

export default function Orders() {
    const [orders, setOrders] = useState([])
    const [loading, setLoading] = useState(true)
    const [search, setSearch] = useState('')
    const [filter, setFilter] = useState('All')
    const [selected, setSelected] = useState([])
    const [showConfirm, setShowConfirm] = useState(false)

    useEffect(() => {
        const fetchOrders = async () => {
            const token = localStorage.getItem('accessToken')
            try {
                const response = await fetch('/atlas/api/order/order', {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
                if (!response.ok) { setLoading(false); return }
                const data = await response.json()
                setOrders(data.map(o => ({
                    id: o.order_id,
                    buyer: o.buyer,
                    seller: o.seller,
                    date: o.issue_date,
                    currency: o.currency,
                    total: o.total,
                    status: o.status || 'Pending',
                    lineCount: o.line_count || 0
                })))
            } catch {
                // silent fail
            } finally {
                setLoading(false)
            }
        }
        fetchOrders()
    }, [])

    const filtered = orders
        .filter(o => filter === 'All' || o.status === filter)
        .filter(o =>
            o.id?.toLowerCase().includes(search.toLowerCase()) ||
            o.buyer?.toLowerCase().includes(search.toLowerCase()) ||
            o.seller?.toLowerCase().includes(search.toLowerCase())
        )

    const toggleSelect = (id) => setSelected(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id])
    const toggleSelectAll = () => setSelected(prev => prev.length === filtered.length ? [] : filtered.map(o => o.id))

    const handleDelete = async () => {
        const token = localStorage.getItem('accessToken')
        await Promise.all(selected.map(id =>
            fetch(`/atlas/api/order/order/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } })
        ))
        setOrders(prev => prev.filter(o => !selected.includes(o.id)))
        setSelected([])
        setShowConfirm(false)
    }

    const statusStyles = {
        Pending: 'bg-yellow-100 text-yellow-700',
        Processing: 'bg-blue-100 text-blue-700',
        Delivered: 'bg-green-100 text-green-700',
    }

    return (
        <SellerDashboardLayout>
            <div className="flex flex-col h-full">
                {showConfirm && (
                    <div className="fixed inset-0 backdrop-blur-[1px] flex items-center justify-center z-50">
                        <div className="bg-white rounded-xl shadow-lg p-6 max-w-sm w-full">
                            <h2 className="text-lg font-semibold mb-2">Delete Orders</h2>
                            <p className="text-gray-500 text-sm mb-6">Are you sure you want to delete {selected.length} order(s)? This action cannot be undone.</p>
                            <div className="flex justify-end gap-3">
                                <button onClick={() => setShowConfirm(false)} className="border border-gray-300 text-gray-600 px-4 py-2 rounded-lg hover:bg-gray-50 text-sm">Cancel</button>
                                <button onClick={handleDelete} className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 text-sm">Delete</button>
                            </div>
                        </div>
                    </div>
                )}

                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-2xl font-bold">Orders</h1>
                    <div className="flex gap-3 items-center">
                        {selected.length > 0 && (
                            <button onClick={() => setShowConfirm(true)} className="border border-red-300 text-red-500 px-4 py-2 rounded-lg hover:bg-red-500 hover:text-white text-sm transition-colors duration-100">
                                Delete ({selected.length})
                            </button>
                        )}
                        <Link to="/create-order">
                            <button className="bg-deep-sky-blue-600 text-white px-4 py-2 rounded-lg hover:bg-deep-sky-blue-700">+ Create Order</button>
                        </Link>
                    </div>
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
                                <th className="px-4 py-3 border-b border-gray-300 w-10">
                                    <input type="checkbox" checked={filtered.length > 0 && selected.length === filtered.length} onChange={toggleSelectAll} className="w-4 h-4" />
                                </th>
                                <th className="px-4 py-3 border-b border-gray-300">Order ID</th>
                                <th className="px-4 py-3 border-b border-gray-300">Buyer</th>
                                <th className="px-4 py-3 border-b border-gray-300">Seller</th>
                                <th className="px-4 py-3 border-b border-gray-300">Date</th>
                                <th className="px-4 py-3 border-b border-gray-300">Items</th>
                                <th className="px-4 py-3 border-b border-gray-300">Total</th>
                                <th className="px-4 py-3 border-b border-gray-300">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading ? (
                                <tr><td colSpan="8" className="px-4 py-8 text-center text-gray-400">Loading...</td></tr>
                            ) : filtered.length === 0 ? (
                                <tr>
                                    <td colSpan="8" className="px-4 py-12 text-center text-gray-400">
                                        <p className="font-medium mb-1">No orders yet</p>
                                        <p className="text-sm">Click Create Order to add your first order.</p>
                                    </td>
                                </tr>
                            ) : (
                                filtered.map((order, index) => (
                                    <tr key={index} className={`hover:bg-gray-50 border-b border-gray-200 ${selected.includes(order.id) ? 'bg-blue-50' : ''}`}>
                                        <td className="px-4 py-3">
                                            <input type="checkbox" checked={selected.includes(order.id)} onChange={() => toggleSelect(order.id)} className="w-4 h-4" />
                                        </td>
                                        <td className="px-4 py-3 text-deep-sky-blue-600 text-sm font-medium">{order.id}</td>
                                        <td className="px-4 py-3 text-sm">{order.buyer}</td>
                                        <td className="px-4 py-3 text-sm">{order.seller}</td>
                                        <td className="px-4 py-3 text-gray-500 text-sm">{order.date}</td>
                                        <td className="px-4 py-3 text-sm text-gray-500">{order.lineCount} item{order.lineCount !== 1 ? 's' : ''}</td>
                                        <td className="px-4 py-3 text-sm font-medium">{order.currency} {order.total}</td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyles[order.status] || 'bg-gray-100 text-gray-600'}`}>{order.status}</span>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </SellerDashboardLayout>
    )
}