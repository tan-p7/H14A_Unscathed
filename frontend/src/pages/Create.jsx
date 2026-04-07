import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/layout'
import { generateDespatch } from '../api/despatch'
import { getToken } from '../api/auth'

function Create() {
  const [xml, setXml] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleSubmit() {
    setLoading(true)
    setError('')
    const res = await generateDespatch(xml, getToken())
    if (res.ok) {
      navigate('/dashboard')
    } else {
      setError('Failed to generate despatch')
    }
    setLoading(false)
  }

  return (
    <Layout>
      <h1>Create Despatch</h1>
      <textarea
        rows={10}
        style={{ width: '100%' }}
        placeholder="Paste UBL Order XML here..."
        value={xml}
        onChange={e => setXml(e.target.value)}
      />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Despatch'}
      </button>
    </Layout>
  )
}

export default Create