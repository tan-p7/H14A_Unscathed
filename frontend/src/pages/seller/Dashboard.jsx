import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

const recentOrders = [
    { id: 'PO-2026-001', customer: 'Acme Corp', date: '2026-04-20', status: 'Pending', total: '$1,200.00' },
    { id: 'PO-2026-002', customer: 'Global Tech', date: '2026-04-19', status: 'Processing', total: '$3,450.00' },
    { id: 'PO-2026-003', customer: 'StartupXYZ', date: '2026-04-18', status: 'Delivered', total: '$780.00' },
]

export default function SellerDashboard() {
    const name = localStorage.getItem('name') || 'there'

    return (
        <SellerDashboardLayout>
            <h1 className="text-2xl font-bold mb-2">Hi, {name} 👋</h1>
            <p className="text-gray-500 mb-8">Here's what's happening with your store today.</p>

            <div className="grid grid-cols-4 gap-6 mb-8">
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">Total Orders</p>
                    <p className="text-3xl font-bold mt-2">24</p>
                    <p className="text-green-500 text-xs mt-1">↑ 12% this month</p>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">Despatch Advices</p>
                    <p className="text-3xl font-bold mt-2">18</p>
                    <p className="text-green-500 text-xs mt-1">↑ 8% this month</p>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">Pending Orders</p>
                    <p className="text-3xl font-bold mt-2">6</p>
                    <p className="text-yellow-500 text-xs mt-1">Requires attention</p>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">Total Revenue</p>
                    <p className="text-3xl font-bold mt-2">$48,200</p>
                    <p className="text-green-500 text-xs mt-1">↑ 20% this month</p>
                </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                <h2 className="text-lg font-semibold mb-4">Recent Orders</h2>
                <table className="w-full border-collapse">
                    <thead>
                        <tr className="text-left text-gray-500 text-sm border-b border-gray-100">
                            <th className="pb-3">Order ID</th>
                            <th className="pb-3">Customer</th>
                            <th className="pb-3">Date</th>
                            <th className="pb-3">Status</th>
                            <th className="pb-3">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {recentOrders.map((order, index) => (
                            <tr key={index} className="border-b border-gray-50 hover:bg-gray-50">
                                <td className="py-3 text-deep-sky-blue-600 text-sm">{order.id}</td>
                                <td className="py-3 text-sm">{order.customer}</td>
                                <td className="py-3 text-gray-500 text-sm">{order.date}</td>
                                <td className="py-3">
                                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                        order.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                                        order.status === 'Processing' ? 'bg-blue-100 text-blue-700' :
                                        'bg-green-100 text-green-700'
                                    }`}>{order.status}</span>
                                </td>
                                <td className="py-3 text-sm">{order.total}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </SellerDashboardLayout>
    )
}