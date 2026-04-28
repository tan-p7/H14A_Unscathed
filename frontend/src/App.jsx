import {BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import Landing from './pages/public/Landing'
import Privacy from './pages/public/Privacy'
import Terms from './pages/public/Terms'
import SellerDashboard from './pages/seller/Dashboard'
import CustomerDashboard from './pages/customer/Dashboard'
import CustomerOrders from './pages/customer/Orders'
import CustomerCreateOrder from './pages/customer/CreateOrder'
import Orders from './pages/seller/Orders'
import CreateOrder from './pages/seller/CreateOrder'
import Despatch from './pages/seller/Despatch'
import ViewDespatch from './pages/seller/ViewDespatch'
import Invoices from './pages/seller/Invoices'
import Settings from './pages/seller/Settings'
import Profile from './pages/seller/Profile'
import CreateDespatch from './pages/seller/CreateDespatch'
import CustomerDespatch from './pages/customer/Despatch'
import CustomerInvoices from './pages/customer/Invoices'
import GenerateInvoice from './pages/seller/GenerateInvoice'
import Pricing from './pages/public/Pricing'
import CustomerSettings from './pages/customer/Settings'

export default function App() {
  return (
    <BrowserRouter basename="/H14A_Unscathed/">
      <Routes>
        <Route path="/" element={<Landing/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/privacy-policy" element={<Privacy/>} />
        <Route path="/terms" element={<Terms/>} />
        <Route path="/pricing" element={<Pricing/>} />

        {/* Seller routes */}
        <Route path="/dashboard" element={<SellerDashboard/>} />
        <Route path="/orders" element={<Orders/>} />
        <Route path="/create-order" element={<CreateOrder/>} />
        <Route path="/despatch" element={<Despatch/>} />
        <Route path="/despatch/:id" element={<ViewDespatch/>} />
        <Route path="/invoices" element={<Invoices/>} />
        <Route path="/settings" element={<Settings/>} />
        <Route path="/profile" element={<Profile/>} />
        <Route path="/create-despatch" element={<CreateDespatch/>} />
        <Route path="/generate-invoice/:id" element={<GenerateInvoice />} />

        {/* Customer routes */}
        <Route path="/customer-dashboard" element={<CustomerDashboard/>} />
        <Route path="/customer-orders" element={<CustomerOrders/>} />
        <Route path="/customer-create-order" element={<CustomerCreateOrder/>} />
        <Route path="/customer-despatch" element={<CustomerDespatch />} />
        <Route path="/customer-invoices" element={<CustomerInvoices />} />
        <Route path="/settings" element={<CustomerSettings />} />
      </Routes>
    </BrowserRouter>
  )
}