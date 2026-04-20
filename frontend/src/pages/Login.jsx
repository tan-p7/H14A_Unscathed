import { useState } from 'react'
import { Link } from 'react-router-dom'


export default function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)
    const handleSubmit = async (event) => {
        event.preventDefault()

        const response = await fetch('/atlas/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        })

        const data = await response.json()

        if (response.status === 200) {
            localStorage.setItem('accessToken', data.accessToken)
            console.log('Logged in successfully')
        } else {
            console.log('Invalid email or password')
        }
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
                        onChange={(event) => setEmail(event.target.value)}/>
                    <div className="relative mb-4">
                        <input 
                            type={showPassword ? 'text' : 'password'}
                            className="w-full border border-gray-300 rounded-lg px-4 py-2 pr-12"
                            placeholder="Password" 
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}/>
                        <button 
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-2 text-gray-500 text-sm">
                            {showPassword ? 'Hide' : 'Show'}
                        </button>
                    </div>
                    <button type="submit" className="w-full bg-deep-sky-blue-600 text-white py-2 rounded-lg hover:bg-deep-sky-blue-700">Log In</button>
                </form>
                <p className="text-sm text-gray-500 mt-4 text-center">Don't have an account? <Link to="/register" className="text-deep-sky-blue-600 hover:underline">Sign up</Link></p>
            </div>
        </div>
    )
}