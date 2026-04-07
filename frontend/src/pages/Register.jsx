import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register } from '../api/despatch'

function Register() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleRegister() {
    setLoading(true)
    setError('')
    const res = await register(email, password, name)
    if (res.ok) {
      navigate('/')
    } else {
      const data = await res.json()
      setError(data || 'Registration failed')
    }
    setLoading(false)
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h2 style={{ fontFamily: "'Sora', sans-serif", fontWeight: 700, color: '#1a6b7a', letterSpacing: '2px' }}>ATLAS</h2>
        <p className="login-subtitle">Create your account</p>
        <div className="form-field">
          <label>Name</label>
          <input type="text" placeholder="Your name" value={name} onChange={e => setName(e.target.value)} />
        </div>
        <div className="form-field">
          <label>Email</label>
          <input type="email" placeholder="you@company.com" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="form-field">
          <label>Password</label>
          <input type="password" placeholder="Min 8 characters" value={password} onChange={e => setPassword(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleRegister()} />
        </div>
        {error && <p style={{ color: 'red', fontSize: '13px' }}>{error}</p>}
        <button className="btn-primary" onClick={handleRegister} disabled={loading}>
          {loading ? 'Creating account...' : 'Sign Up'}
        </button>
        <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '13px' }}>
          Already have an account?{' '}
          <span style={{ color: '#2389a0', fontWeight: 600, cursor: 'pointer' }} onClick={() => navigate('/')}>Sign in</span>
        </p>
      </div>
    </div>
  )
}

export default Register