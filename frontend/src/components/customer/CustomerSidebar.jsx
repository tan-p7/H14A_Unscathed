import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function CustomerSidebar() {
    const [collapsed, setCollapsed] = useState(false)
    const navigate = useNavigate()

    const token = localStorage.getItem('accessToken')
    const roles = JSON.parse(localStorage.getItem('roles') || '["customer"]')
    const hasBothRoles = roles.includes('customer') && roles.includes('seller')
    const name = localStorage.getItem('name') || ''

    let email = ''
    try {
        email = JSON.parse(atob(token.split('.')[1])).email
    } catch {}

    const displayName = name || email
    const initials = displayName ? displayName[0].toUpperCase() : '?'

    const switchRole = () => {
        localStorage.setItem('activeRole', 'seller')
        navigate('/dashboard')
    }

    return (
        <div className={`flex flex-col bg-gray-50 border-r border-gray-200 h-screen transition-all duration-300 ${collapsed ? 'w-16' : 'w-64'}`}>
            <div className={`flex items-center border-b border-gray-200 p-4 ${collapsed ? 'justify-center' : 'justify-between'}`}>
                {!collapsed && <span className="font-conthrax text-2xl">Atlas</span>}
                <button onClick={() => setCollapsed(!collapsed)} className="text-gray-500 hover:text-gray-800">☰</button>
            </div>
            <nav className="flex flex-col gap-1 p-2 mt-2 flex-1">
                <Link to="/customer-dashboard" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-200 text-gray-700">
                    <span>🏠</span>
                    {!collapsed && <span>Dashboard</span>}
                </Link>
                <Link to="/customer-orders" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-200 text-gray-700">
                    <span>📦</span>
                    {!collapsed && <span>My Orders</span>}
                </Link>
                <Link to="/customer-create-order" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-200 text-gray-700">
                    <span>➕</span>
                    {!collapsed && <span>Place Order</span>}
                </Link>
                <Link to="/customer-despatch" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-200 text-gray-700">
                    <span>🚚</span>
                    {!collapsed && <span>Deliveries</span>}
                </Link>
                <Link to="/customer-invoices" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-200 text-gray-700">
                    <span>🧾</span>
                    {!collapsed && <span>Invoices</span>}
                </Link>
                <Link to="/settings" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-200 text-gray-700">
                    <span>⚙️</span>
                    {!collapsed && <span>Settings</span>}
                </Link>
            </nav>

            <div className="border-t border-gray-200 p-3">
                {!collapsed && (
                    <div className="flex items-center gap-3 mb-3">
                        <div className="w-8 h-8 rounded-full bg-deep-sky-blue-600 flex items-center justify-center text-white text-sm font-medium flex-shrink-0">
                            {initials}
                        </div>
                        <div className="overflow-hidden">
                            <p className="text-sm text-gray-800 truncate">{displayName}</p>
                            <p className="text-xs text-gray-400">Customer Account</p>
                        </div>
                    </div>
                )}
                {hasBothRoles && !collapsed && (
                    <button
                        onClick={switchRole}
                        className="w-full bg-white border border-gray-300 text-gray-700 text-sm font-medium px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        Go to Seller Portal
                    </button>
                )}
            </div>
        </div>
    )
}