import '../styles/Login.css'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../api/despatch'
import { saveToken } from '../api/auth'

function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleLogin() {
    setLoading(true)
    setError('')
    const res = await login(email, password)
    if (res.ok) {
      const data = await res.json()
      saveToken(data.accessToken)
      navigate('/home')
    } else {
      setError('Invalid email or password')
    }
    setLoading(false)
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h2 style={{ fontFamily: "'Sora', sans-serif", fontWeight: 700, color: '#1a6b7a', letterSpacing: '2px' }}>ATLAS</h2>
        <p className="login-subtitle">Shipping, Simplified</p>

        <div className="form-field">
          <label>Email</label>
          <input
            type="email"
            placeholder="you@company.com"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
        </div>

        <div className="form-field">
          <label>Password</label>
          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={e => setPassword(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
          />
        </div>

        {error && <p style={{ color: 'red', fontSize: '13px', marginBottom: '8px' }}>{error}</p>}

        <button className="btn-primary" onClick={handleLogin} disabled={loading}>
          {loading ? 'Signing in...' : 'Sign In'}
        </button>

        <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '13px' }}>
          Don't have an account?{' '}
          <span
            style={{ color: '#2389a0', fontWeight: 600, cursor: 'pointer' }}
            onClick={() => navigate('/register')}
          >
            Sign up
          </span>
        </p>

        <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '12px' }}>
          By using Atlas, you agree to our{' '}
          <span onClick={() => navigate('/terms')} style={{ cursor: 'pointer', color: '#2389a0' }}>
            Terms
          </span>{' '}
          and{' '}
          <span onClick={() => navigate('/privacy')} style={{ cursor: 'pointer', color: '#2389a0' }}>
            Privacy Policy
          </span>
        </p>
      </div>
    </div>
  )
}

export default Login