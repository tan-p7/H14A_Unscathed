import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Layout from '../components/layout'
import { getDespatch, deleteDespatch } from '../api/despatch'
import { getToken } from '../api/auth'

function ViewDespatch() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [xml, setXml] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetch() {
      const res = await getDespatch(id, getToken())
      if (res.ok) setXml(await res.text())
      else setError('Failed to load despatch')
    }
    fetch()
  }, [id])

  async function handleDelete() {
    await deleteDespatch(id, getToken())
    navigate('/dashboard')
  }

  return (
    <Layout>
      <h1>Despatch {id}</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <pre>{xml}</pre>
      <button onClick={handleDelete}>Delete</button>
    </Layout>
  )
}

export default ViewDespatch