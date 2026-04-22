import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

const STANDARDS = [
    { code: 'AU', label: 'Australia', standard: 'PEPPOL BIS Billing 3.0', description: 'Mandatory for Australian government, widely adopted by businesses' },
    { code: 'NZ', label: 'New Zealand', standard: 'PEPPOL BIS Billing 3.0', description: 'New Zealand e-invoicing mandate via PEPPOL network' },
    { code: 'SG', label: 'Singapore', standard: 'InvoiceNow (PEPPOL)', description: 'Singapore nationwide e-invoicing network based on PEPPOL' },
    { code: 'EU', label: 'European Union', standard: 'EN 16931', description: 'European standard for electronic invoicing' },
    { code: 'US', label: 'United States', standard: 'UBL 2.1', description: 'OASIS Universal Business Language standard' },
]

export default function GenerateInvoice() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [step, setStep] = useState(1)

    return (
        <SellerDashboardLayout>
            <div className="flex items-center gap-4 mb-8">
                <button onClick={() => navigate(`/despatch/${id}`)} className="text-gray-500 hover:text-gray-700 text-sm">← Back</button>
                <h1 className="text-2xl font-bold">Generate Invoice</h1>
            </div>

            <div className="flex items-center gap-2 mb-8">
                {['Select Standard', 'Invoice Details', 'Review & Download'].map((label, index) => (
                    <div key={index} className="flex items-center gap-2">
                        <div className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-medium ${step > index + 1 ? 'bg-green-500 text-white' : step === index + 1 ? 'bg-deep-sky-blue-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
                            {step > index + 1 ? '✓' : index + 1}
                        </div>
                        <span className={`text-sm ${step === index + 1 ? 'text-deep-sky-blue-600 font-medium' : 'text-gray-400'}`}>{label}</span>
                        {index < 2 && <div className="w-12 h-px bg-gray-200 mx-1" />}
                    </div>
                ))}
            </div>

            <p className="text-gray-400">Step {step} coming soon...</p>
        </SellerDashboardLayout>
    )
}