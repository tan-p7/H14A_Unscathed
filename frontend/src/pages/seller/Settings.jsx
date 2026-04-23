import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

export default function Settings() {
    const [emailNotifications, setEmailNotifications] = useState(true)
    const [orderAlerts, setOrderAlerts] = useState(true)
    const [despatchAlerts, setDespatchAlerts] = useState(false)
    const [invoiceAlerts, setInvoiceAlerts] = useState(true)
    const [currency, setCurrency] = useState('AUD')
    const [timezone, setTimezone] = useState('Australia/Sydney')
    const navigate = useNavigate()

    return (
        <SellerDashboardLayout>
            <h1 className="text-2xl font-bold mb-8">Settings</h1>
            <div className="max-w-2xl flex flex-col gap-6">

                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Preferences</h2>
                    <div className="flex flex-col gap-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-700">Currency</p>
                                <p className="text-xs text-gray-400">Default currency for orders and invoices</p>
                            </div>
                            <select value={currency} onChange={(e) => setCurrency(e.target.value)} className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
                                <option value="AUD">AUD</option>
                                <option value="USD">USD</option>
                                <option value="GBP">GBP</option>
                                <option value="EUR">EUR</option>
                                <option value="SGD">SGD</option>
                            </select>
                        </div>
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-700">Timezone</p>
                                <p className="text-xs text-gray-400">Used for date and time display</p>
                            </div>
                            <select value={timezone} onChange={(e) => setTimezone(e.target.value)} className="border border-gray-300 rounded-lg px-3 py-2 text-sm">
                                <option value="Australia/Sydney">Sydney (AEST)</option>
                                <option value="Australia/Melbourne">Melbourne (AEST)</option>
                                <option value="Australia/Perth">Perth (AWST)</option>
                                <option value="Pacific/Auckland">Auckland (NZST)</option>
                                <option value="Asia/Singapore">Singapore (SGT)</option>
                                <option value="America/New_York">New York (EST)</option>
                                <option value="Europe/London">London (GMT)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Notifications</h2>
                    <div className="flex flex-col gap-4">
                        {[
                            { label: 'Email Notifications', desc: 'Receive notifications via email', value: emailNotifications, setter: setEmailNotifications },
                            { label: 'New Order Alerts', desc: 'Get notified when a new order is placed', value: orderAlerts, setter: setOrderAlerts },
                            { label: 'Despatch Advice Alerts', desc: 'Get notified when a despatch is updated', value: despatchAlerts, setter: setDespatchAlerts },
                            { label: 'Invoice Alerts', desc: 'Get notified when an invoice is paid or overdue', value: invoiceAlerts, setter: setInvoiceAlerts },
                        ].map((item, index) => (
                            <div key={index} className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-700">{item.label}</p>
                                    <p className="text-xs text-gray-400">{item.desc}</p>
                                </div>
                                <button
                                    onClick={() => item.setter(!item.value)}
                                    className={`w-10 h-6 rounded-full transition-colors duration-200 ${item.value ? 'bg-deep-sky-blue-600' : 'bg-gray-300'}`}
                                >
                                    <div className={`w-4 h-4 bg-white rounded-full shadow transition-transform duration-200 mx-1 ${item.value ? 'translate-x-4' : 'translate-x-0'}`} />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="flex justify-end">
                    <button className="bg-deep-sky-blue-600 text-white px-6 py-2 rounded-lg hover:bg-deep-sky-blue-700">
                        Save Changes
                    </button>
                </div>
            </div>
        </SellerDashboardLayout>
    )
}