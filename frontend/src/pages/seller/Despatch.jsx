import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

const API = import.meta.env.VITE_API_URL ?? '/atlas'

export default function Despatch() {
    const [despatchList, setDespatchList] = useState([])
    const [search, setSearch] = useState('')
    const [filter, setFilter] = useState('All')
    const [loading, setLoading] = useState(true)
    const [selected, setSelected] = useState([])
    const [showConfirm, setShowConfirm] = useState(false)
    const [showStatusMenu, setShowStatusMenu] = useState(false)
    const [statusUpdating, setStatusUpdating] = useState(false)

    useEffect(() => {
        const fetchDespatches = async () => {
            const token = localStorage.getItem('accessToken')
            const response = await fetch(`${API}/api/despatch/despatch-advice`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (!response.ok) { setLoading(false); return }
            const xmlText = await response.text()
            const matches = xmlText.match(/<ns0:DespatchAdvice[\s\S]*?<\/ns0:DespatchAdvice>/g) || []
            const parsed = matches.map(advice => {
                const idMatch = advice.match(/<ns1:ID>(.*?)<\/ns1:ID>/)
                const dateMatch = advice.match(/<ns1:IssueDate>(.*?)<\/ns1:IssueDate>/)
                const orderRefMatch = advice.match(/<ns2:OrderReference>[\s\S]*?<ns1:ID>(.*?)<\/ns1:ID>/)
                const statusMatch = advice.match(/<ns1:DocumentStatusCode>(.*?)<\/ns1:DocumentStatusCode>/)
                const rawStatus = statusMatch?.[1] || 'NoStatus'
                const status = rawStatus === 'NoStatus' ? 'Pending' : rawStatus
                return { id: idMatch?.[1] || '', date: dateMatch?.[1] || '', orderId: orderRefMatch?.[1] || '', status }
            })
            setDespatchList(parsed)
            setLoading(false)
        }
        fetchDespatches()
    }, [])

    const filteredDespatch = despatchList
        .filter(d => filter === 'All' || d.status === filter)
        .filter(d => d.id.toLowerCase().includes(search.toLowerCase()) || d.orderId.toLowerCase().includes(search.toLowerCase()))

    const toggleSelect = (id) => setSelected(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id])
    const toggleSelectAll = () => setSelected(prev => prev.length === filteredDespatch.length ? [] : filteredDespatch.map(d => d.id))

    const handleDeleteSelected = async () => {
        const token = localStorage.getItem('accessToken')
        await Promise.all(selected.map(id => fetch(`${API}/api/despatch/despatch-advice/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } })))
        setDespatchList(prev => prev.filter(d => !selected.includes(d.id)))
        setSelected([])
        setShowConfirm(false)
    }

    const handleStatusChange = async (newStatus) => {
        setStatusUpdating(true)
        setShowStatusMenu(false)
        const token = localStorage.getItem('accessToken')
        await Promise.all(selected.map(id =>
            fetch(`${API}/api/despatch/despatch-advice/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                body: JSON.stringify({ status: newStatus })
            })
        ))
        setDespatchList(prev => prev.map(d => selected.includes(d.id) ? { ...d, status: newStatus } : d))
        setSelected([])
        setStatusUpdating(false)
    }

    const statusStyles = {
        Pending: 'bg-yellow-100 text-yellow-700',
        Shipped: 'bg-blue-100 text-blue-700',
        Delivered: 'bg-green-100 text-green-700',
    }

    return (
        <SellerDashboardLayout>
            <div className="flex flex-col h-full">
                {showConfirm && (
                    <div className="fixed inset-0 backdrop-blur-[1px] flex items-center justify-center z-50">
                        <div className="bg-white rounded-xl shadow-lg p-6 max-w-sm w-full">
                            <h2 className="text-lg font-semibold mb-2">Delete Despatch Advice</h2>
                            <p className="text-gray-500 text-sm mb-6">Are you sure you want to delete {selected.length} despatch advice(s)? This action cannot be undone.</p>
                            <div className="flex justify-end gap-3">
                                <button onClick={() => setShowConfirm(false)} className="border border-gray-300 text-gray-600 px-4 py-2 rounded-lg hover:bg-gray-50 text-sm">Cancel</button>
                                <button onClick={handleDeleteSelected} className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 text-sm">Delete</button>
                            </div>
                        </div>
                    </div>
                )}

                <div className="flex justify-between items-center mb-4">
                    <h1 className="text-2xl font-bold">Despatch Advice</h1>
                    <div className="flex gap-3 items-center">
                        {selected.length > 0 && (
                            <>
                                {/* Status dropdown */}
                                <div className="relative">
                                    <button
                                        onClick={() => setShowStatusMenu(prev => !prev)}
                                        disabled={statusUpdating}
                                        className="border border-gray-300 text-gray-600 px-4 py-2 rounded-lg hover:bg-gray-50 text-sm disabled:opacity-50"
                                    >
                                        {statusUpdating ? 'Updating...' : `Set Status (${selected.length}) ▾`}
                                    </button>
                                    {showStatusMenu && (
                                        <div className="absolute right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10 w-36">
                                            {['Pending', 'Shipped', 'Delivered'].map(s => (
                                                <button
                                                    key={s}
                                                    onClick={() => handleStatusChange(s)}
                                                    className="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 first:rounded-t-lg last:rounded-b-lg"
                                                >
                                                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusStyles[s]}`}>{s}</span>
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                <button onClick={() => setShowConfirm(true)} className="border border-red-300 text-red-500 px-4 py-2 rounded-lg hover:bg-red-500 hover:text-white text-sm transition-colors duration-100">
                                    Delete ({selected.length})
                                </button>
                            </>
                        )}
                        <Link to="/create-despatch">
                            <button className="bg-deep-sky-blue-600 text-white px-4 py-2 rounded-lg hover:bg-deep-sky-blue-700">+ Create Despatch</button>
                        </Link>
                    </div>
                </div>

                <div className="flex gap-4 mb-4">
                    <input type="text" placeholder="Search despatch..." value={search} onChange={(e) => setSearch(e.target.value)} className="border border-gray-300 rounded-lg px-4 py-2 w-64" />
                    <div className="flex gap-2">
                        {['All', 'Pending', 'Shipped', 'Delivered'].map((status) => (
                            <button key={status} onClick={() => setFilter(status)} className={`px-4 py-2 rounded-md text-sm ${filter === status ? 'bg-deep-sky-blue-600 text-white' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'}`}>{status}</button>
                        ))}
                    </div>
                </div>

                <div className="rounded-xl shadow-sm border border-gray-300 overflow-hidden flex-1 overflow-y-auto">
                    <table className="w-full border-collapse">
                        <thead className="sticky top-0 bg-gray-200">
                            <tr className="text-left text-gray-600 text-sm">
                                <th className="px-4 py-3 border-b border-gray-300 w-10"><input type="checkbox" checked={filteredDespatch.length > 0 && selected.length === filteredDespatch.length} onChange={toggleSelectAll} className="w-4 h-4" /></th>
                                <th className="px-4 py-3 border-b border-gray-300">Despatch ID</th>
                                <th className="px-4 py-3 border-b border-gray-300">Order ID</th>
                                <th className="px-4 py-3 border-b border-gray-300">Date</th>
                                <th className="px-4 py-3 border-b border-gray-300">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading ? (
                                <tr><td colSpan="5" className="px-4 py-8 text-center text-gray-400">Loading...</td></tr>
                            ) : filteredDespatch.length === 0 ? (
                                <tr><td colSpan="5" className="px-4 py-8 text-center text-gray-400">No despatch advices found.</td></tr>
                            ) : (
                                filteredDespatch.map((d, index) => (
                                    <tr key={index} className={`hover:bg-gray-50 border-b border-gray-200 ${selected.includes(d.id) ? 'bg-blue-50' : ''}`}>
                                        <td className="px-4 py-3"><input type="checkbox" checked={selected.includes(d.id)} onChange={() => toggleSelect(d.id)} className="w-4 h-4" /></td>
                                        <td className="px-4 py-3 text-deep-sky-blue-600"><Link to={`/despatch/${d.id}`}>{d.id}</Link></td>
                                        <td className="px-4 py-3">{d.orderId}</td>
                                        <td className="px-4 py-3 text-gray-500">{d.date}</td>
                                        <td className="px-4 py-3">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyles[d.status] || 'bg-gray-100 text-gray-600'}`}>{d.status}</span>
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