import {BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Landing from './pages/Landing'
import Privacy from './pages/Privacy'
import Terms from './pages/Terms'
import Dashboard from './pages/Dashboard'
import Orders from './pages/Orders'
import CreateOrder from './pages/CreateOrder'
import Despatch from './pages/Despatch'

export  default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/privacy-policy" element={<Privacy/>} />
        <Route path="/terms" element={<Terms/>} />
        <Route path="/dashboard" element={<Dashboard/>} />
        <Route path="/orders" element={<Orders/>} />
        <Route path="/create-order" element={<CreateOrder/>} />
        <Route path="/despatch" element={<Despatch/>} />
      </Routes>
    </BrowserRouter>
  )
}