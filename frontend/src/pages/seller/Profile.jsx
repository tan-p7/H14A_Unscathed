import SellerDashboardLayout from '../../components/seller/SellerDashboardLayout'

export default function Profile() {
    const token = localStorage.getItem('accessToken')
    const email = token ? JSON.parse(atob(token.split('.')[1])).email : 'User'

    return (
        <SellerDashboardLayout>
            <h1 className="text-2xl font-bold mb-8">Profile</h1>
            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm max-w-lg">
                <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 rounded-full bg-deep-sky-blue-600 flex items-center justify-center text-white text-2xl">
                        {email[0].toUpperCase()}
                    </div>
                    <div>
                        <p className="font-semibold">{email}</p>
                        <p className="text-gray-400 text-sm">Account details</p>
                    </div>
                </div>
                <div className="flex flex-col gap-4">
                    <input type="text" placeholder="Name" className="w-full border border-gray-300 rounded-lg px-4 py-2" />
                    <input type="email" placeholder="Email" defaultValue={email} className="w-full border border-gray-300 rounded-lg px-4 py-2" />
                    <div className="flex justify-end">
                        <button className="bg-deep-sky-blue-600 text-white px-6 py-2 rounded-lg hover:bg-deep-sky-blue-700">Save Changes</button>
                    </div>
                </div>
            </div>
        </SellerDashboardLayout>
    )
}