import { useState } from 'react'

export default function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const handleSubmit = async (event) => {
        event.preventDefault()

         const response = await fetch('/atlas/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        })

        console.log(email, password)
        }
    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <input type="email" placeholder="Email" value={email}
                    onChange={(event) => setEmail(event.target.value)}/>
                <input type="password" placeholder="Password" value={password}
                    onChange={(event) => setPassword(event.target.value)}/>
                <button type="submit">Log in</button>
            </form>
        </div>
    )
}