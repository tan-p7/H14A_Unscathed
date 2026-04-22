import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function NavbarLoggedIn({ dark = false }) {
    const navigate = useNavigate()
    const [dropdownOpen, setDropdownOpen] = useState(false)

    const token = localStorage.getItem('accessToken')
    const activeRole = localStorage.getItem('activeRole') || 'customer'

    let email = ''
    try {
        email = JSON.parse(atob(token.split('.')[1])).email
    } catch {}

    const handleLogout = () => {
        localStorage.clear()
        navigate('/login')
    }

    const initials = email ? email[0].toUpperCase() : '?'

    return (
        <div className={`flex items-center justify-between px-6 py-3 border-b ${dark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
            <span className={`font-conthrax text-xl ${dark ? 'text-white' : 'text-deep-sky-blue-600'}`}>Atlas</span>
            <div className="flex items-center gap-4">
                <div className="relative">
                    <button
                        onClick={() => setDropdownOpen(!dropdownOpen)}
                        className="flex items-center gap-2"
                    >
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium text-white ${dark ? 'bg-gray-600' : 'bg-deep-sky-blue-600'}`}>
                            {initials}
                        </div>
                        <span className={`text-sm ${dark ? 'text-gray-300' : 'text-gray-600'}`}>
                            Hi, {localStorage.getItem('name') || email}
                        </span>
                    </button>
                    {dropdownOpen && (
                        <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-xl shadow-lg z-50">
                            <div className="px-4 py-2 border-b border-gray-100">
                                <p className="text-xs text-gray-400">Signed in as</p>
                                <p className="text-sm font-medium truncate">{email}</p>
                                <p className="text-xs text-deep-sky-blue-600 capitalize">{activeRole}</p>
                            </div>
                            <button
                                onClick={() => { setDropdownOpen(false); navigate('/profile') }}
                                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                            >
                                Profile
                            </button>
                            <button
                                onClick={() => { setDropdownOpen(false); navigate('/settings') }}
                                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                            >
                                Settings
                            </button>
                            <button
                                onClick={handleLogout}
                                className="w-full text-left px-4 py-2 text-sm text-red-500 hover:bg-gray-50 rounded-b-xl"
                            >
                                Logout
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}