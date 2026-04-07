import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Create from './pages/Create'
import ViewDespatch from './pages/ViewDespatch'
import PrivateRoute from './components/privateroute'
import Register from './pages/Register'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<PrivateRoute><Home /></PrivateRoute>} />
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/create" element={<PrivateRoute><Create /></PrivateRoute>} />
        <Route path="/despatch/:id" element={<PrivateRoute><ViewDespatch /></PrivateRoute>} />
        <Route path="*" element={<Navigate to="/" />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App