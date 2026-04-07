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

  return <div>Register</div>
}

export default Register