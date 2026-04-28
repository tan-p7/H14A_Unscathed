import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function SellerSidebar() {
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
        localStorage.setItem('activeRole', 'customer')
        navigate('/customer-dashboard')
    }

    return (
        <div className={`flex flex-col bg-gray-900 border-r border-gray-700 h-screen transition-all duration-300 ${collapsed ? 'w-16' : 'w-64'}`}>
            <div className={`flex items-center border-b border-gray-700 p-4 ${collapsed ? 'justify-center' : 'justify-between'}`}>
                {!collapsed && <span className="font-conthrax text-3xl text-white">Atlas</span>}
                <button onClick={() => setCollapsed(!collapsed)} className="text-gray-400 hover:text-white">☰</button>
            </div>
            <nav className="flex flex-col gap-1 p-2 mt-2 flex-1">
                <Link to="/dashboard" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-700 text-gray-300">
                    <span>🏠</span>
                    {!collapsed && <span>Dashboard</span>}
                </Link>
                <Link to="/orders" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-700 text-gray-300">
                    <span>📦</span>
                    {!collapsed && <span>Orders</span>}
                </Link>
                <Link to="/despatch" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-700 text-gray-300">
                    <span>🚚</span>
                    {!collapsed && <span>Despatch Advice</span>}
                </Link>
                <Link to="/invoices" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-700 text-gray-300">
                    <span>🧾</span>
                    {!collapsed && <span>Invoices</span>}
                </Link>
                <Link to="/settings" className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-700 text-gray-300">
                    <span>⚙️</span>
                    {!collapsed && <span>Settings</span>}
                </Link>
            </nav>

            <div className="border-t border-gray-700 p-3">
                {!collapsed && (
                    <div className="flex items-center gap-3 mb-3">
                        <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-white text-sm font-medium flex-shrink-0">
                            {initials}
                        </div>
                        <div className="overflow-hidden">
                            <p className="text-sm text-white truncate">{displayName}</p>
                            <p className="text-xs text-gray-400">Seller Account</p>
                        </div>
                    </div>
                )}
                {hasBothRoles && !collapsed && (
                    <button
                        onClick={switchRole}
                        className="w-full bg-white text-gray-800 text-sm font-medium px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                        Go to Customer Portal
                    </button>
                )}
            </div>
        </div>
    )
}