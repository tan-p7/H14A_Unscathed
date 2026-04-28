import CustomerDashboardLayout from '../../components/customer/CustomerDashboardLayout'
import { Link } from 'react-router-dom'

const recentOrders = [
    { id: 'PO-2026-008', date: '2026-04-20', status: 'Pending', total: '$540.00' },
    { id: 'PO-2026-005', date: '2026-04-15', status: 'Delivered', total: '$1,200.00' },
    { id: 'PO-2026-003', date: '2026-04-10', status: 'Delivered', total: '$320.00' },
]

export default function CustomerDashboard() {
    const name = localStorage.getItem('name') || 'there'

    return (
        <CustomerDashboardLayout>
            <h1 className="text-2xl font-bold mb-2">Hi, {name} 👋</h1>
            <p className="text-gray-500 mb-8">Here's a summary of your account.</p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">My Orders</p>
                    <p className="text-3xl font-bold mt-2">8</p>
                    <p className="text-gray-400 text-xs mt-1">All time</p>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">Pending Deliveries</p>
                    <p className="text-3xl font-bold mt-2">2</p>
                    <p className="text-yellow-500 text-xs mt-1">In transit</p>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">Invoices</p>
                    <p className="text-3xl font-bold mt-2">5</p>
                    <p className="text-gray-400 text-xs mt-1">1 unpaid</p>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <p className="text-gray-500 text-sm">Total Spent</p>
                    <p className="text-3xl font-bold mt-2">$4,820</p>
                    <p className="text-gray-400 text-xs mt-1">All time</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-lg font-semibold">Recent Orders</h2>
                        <Link to="/customer-orders" className="text-deep-sky-blue-600 text-sm hover:underline">View all</Link>
                    </div>
                    <table className="w-full border-collapse">
                        <thead>
                            <tr className="text-left text-gray-600 text-sm border-b border-gray-200">
                                <th className="pb-3">Order ID</th>
                                <th className="pb-3">Date</th>
                                <th className="pb-3">Status</th>
                                <th className="pb-3">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentOrders.map((order, index) => (
                                <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                                    <td className="py-3 text-deep-sky-blue-600 text-sm">{order.id}</td>
                                    <td className="py-3 text-gray-500 text-sm">{order.date}</td>
                                    <td className="py-3">
                                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                            order.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                                            'bg-green-100 text-green-700'
                                        }`}>{order.status}</span>
                                    </td>
                                    <td className="py-3 text-sm">{order.total}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                    <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
                    <div className="flex flex-col gap-3">
                        <Link to="/customer-create-order">
                            <button className="w-full bg-deep-sky-blue-600 text-white py-3 rounded-lg hover:bg-deep-sky-blue-700 text-sm font-medium">
                                + Place New Order
                            </button>
                        </Link>
                        <Link to="/customer-orders">
                            <button className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 text-sm font-medium">
                                View My Orders
                            </button>
                        </Link>
                        <Link to="/customer-despatch">
                            <button className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 text-sm font-medium">
                                Track Deliveries
                            </button>
                        </Link>
                        <Link to="/customer-invoices">
                            <button className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg hover:bg-gray-50 text-sm font-medium">
                                View Invoices
                            </button>
                        </Link>
                    </div>
                </div>
            </div>
        </CustomerDashboardLayout>
    )
}