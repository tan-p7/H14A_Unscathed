import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/layout'
import { getAllDespatches } from '../api/despatch'
import { getToken } from '../api/auth'

function Dashboard() {
  const [despatches, setDespatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchAll() {
      const res = await getAllDespatches(getToken())
      if (res.ok) {
        const text = await res.text()
        setDespatches([text])
      } else {
        setError('Failed to load despatches')
      }
      setLoading(false)
    }
    fetchAll()
  }, [])

  return (
    <Layout>
      <h1>Dashboard</h1>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      <button onClick={() => navigate('/create')}>+ New Despatch</button>
      {despatches.length === 0 && !loading && <p>No despatches found</p>}
    </Layout>
  )
}

export default Dashboard