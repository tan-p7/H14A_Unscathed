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

  return <Layout><h1>Create Despatch</h1></Layout>
}

export default Create