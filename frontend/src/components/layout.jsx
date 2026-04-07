import { useNavigate } from 'react-router-dom'

function Layout({ children }) {
  const navigate = useNavigate()

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <nav style={{ width: '220px', background: '#0d4f5c', display: 'flex', flexDirection: 'column', padding: '24px 12px' }}>
        <div style={{ color: 'white', fontFamily: 'Sora', fontWeight: 700, fontSize: '20px', marginBottom: '32px', paddingLeft: '12px' }}>
          ATLAS
        </div>
        <button onClick={() => navigate('/home')}>Home</button>
        <button onClick={() => navigate('/dashboard')}>Dashboard</button>
        <button onClick={() => navigate('/create')}>Create</button>
      </nav>
      <main style={{ flex: 1, padding: '28px' }}>
        {children}
      </main>
    </div>
  )
}

export default Layout