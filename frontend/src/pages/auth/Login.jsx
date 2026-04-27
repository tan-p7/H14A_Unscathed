import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

const API = import.meta.env.VITE_API_URL ?? '/atlas'

export default function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState('')
    const [view, setView] = useState('login') // 'login' | 'forgot' | 'sent'
    const [forgotEmail, setForgotEmail] = useState('')
    const [forgotError, setForgotError] = useState('')
    const [forgotLoading, setForgotLoading] = useState(false)
    const navigate = useNavigate()
    
    const handleSubmit = async (event) => {
        event.preventDefault()
        setError('')

        const response = await fetch(`${API}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        })

        const data = await response.json()

        if (response.status === 200) {
            localStorage.removeItem('token')
            localStorage.setItem('accessToken', data.accessToken)
            localStorage.setItem('name', data.name || '')
            const roles = data.roles || ['customer']
            localStorage.setItem('roles', JSON.stringify(roles))
            const activeRole = roles.includes('seller') ? 'seller' : 'customer'
            localStorage.setItem('activeRole', activeRole)
            navigate('/dashboard')
        } else {
            setError('Invalid email or password')
        }
    }

    const handleForgotPassword = async (event) => {
        event.preventDefault()
        setForgotError('')
        setForgotLoading(true)

        try {
            const response = await fetch(`${API}/auth/forgot-password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: forgotEmail })
            })

            if (response.ok) {
                setView('sent')
            } else {
                setForgotError('Something went wrong. Please try again.')
            }
        } catch {
            setForgotError('Something went wrong. Please try again.')
        } finally {
            setForgotLoading(false)
        }
    }

    if (view === 'forgot') {
        return (
            <div
                className="min-h-screen flex items-center justify-center"
                style={{
                    backgroundImage: `url('${import.meta.env.BASE_URL}babyblue_background.jpg')`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center'
                }}
            >
                <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
                    <h1 className="font-conthrax text-6xl mb-5 text-center">Atlas</h1>
                    <p className="text-gray-800 font-semibold text-center mb-1">Reset your password</p>
                    <p className="text-gray-500 text-sm text-center mb-6">Enter your email and we'll send you a reset link.</p>
                    <form onSubmit={handleForgotPassword}>
                        <input
                            type="email"
                            className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4"
                            placeholder="Email"
                            value={forgotEmail}
                            onChange={(e) => setForgotEmail(e.target.value)}
                            required
                        />
                        {forgotError && <p className="text-red-500 text-sm mb-4">{forgotError}</p>}
                        <button
                            type="submit"
                            disabled={forgotLoading}
                            className="w-full bg-deep-sky-blue-600 text-white py-2 rounded-lg hover:bg-deep-sky-blue-700 disabled:opacity-50"
                        >
                            {forgotLoading ? 'Sending...' : 'Send reset link'}
                        </button>
                    </form>
                    <button
                        onClick={() => setView('login')}
                        className="text-sm text-deep-sky-blue-600 hover:underline mt-4 w-full text-center block"
                    >
                        ← Back to login
                    </button>
                </div>
            </div>
        )
    }

    if (view === 'sent') {
        return (
            <div
                className="min-h-screen flex items-center justify-center"
                style={{
                    backgroundImage: "url('/babyblue_background.jpg')",
                    backgroundSize: 'cover',
                    backgroundPosition: 'center'
                }}
            >
                <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md text-center">
                    <h1 className="font-conthrax text-6xl mb-5 text-center">Atlas</h1>
                    <div className="text-4xl mb-4">📧</div>
                    <p className="text-gray-800 font-semibold mb-2">Check your email</p>
                    <p className="text-gray-500 text-sm mb-6">
                        We sent a password reset link to <span className="font-medium text-gray-700">{forgotEmail}</span>. It may take a minute to arrive.
                    </p>
                    <button
                        onClick={() => setView('login')}
                        className="text-sm text-deep-sky-blue-600 hover:underline"
                    >
                        ← Back to login
                    </button>
                </div>
            </div>
        )
    }

    return (
        <div
            className="min-h-screen flex items-center justify-center"
            style={{
                backgroundImage: "url('/babyblue_background.jpg')",
                backgroundSize: 'cover',
                backgroundPosition: 'center'
            }}
        >
            <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
                <h1 className="font-conthrax text-6xl mb-5 text-center">Atlas</h1>
                <p className="text-gray-500 mb-4 text-center">Sign in to your account</p>
                <form onSubmit={handleSubmit}>
                    <input type="email" className="w-full border border-gray-300 rounded-lg px-4 py-2 mb-4" placeholder="Email" value={email}
                        onChange={(event) => setEmail(event.target.value)} />
                    <div className="relative mb-2">
                        <input
                            type={showPassword ? 'text' : 'password'}
                            className="w-full border border-gray-300 rounded-lg px-4 py-2 pr-12"
                            placeholder="Password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)} />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-2 text-gray-500 text-sm">
                            {showPassword ? 'Hide' : 'Show'}
                        </button>
                    </div>
                    <div className="flex justify-end mb-4">
                        <button
                            type="button"
                            onClick={() => setView('forgot')}
                            className="text-xs text-deep-sky-blue-600 hover:underline"
                        >
                            Forgot password?
                        </button>
                    </div>
                    {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
                    <button type="submit" className="w-full bg-deep-sky-blue-600 text-white py-2 rounded-lg hover:bg-deep-sky-blue-700">Log In</button>
                </form>
                <p className="text-sm text-gray-500 mt-4 text-center">Don't have an account? <Link to="/register" className="text-deep-sky-blue-600 hover:underline">Sign up</Link></p>
            </div>
        </div>
    )
}