import SellerSidebar from './SellerSidebar'
import NavbarLoggedIn from '../shared/NavbarLoggedIn'

export default function SellerDashboardLayout({ children }) {
    return (
        <div className="flex h-screen">
            <SellerSidebar />
            <div className="flex flex-col flex-1 overflow-hidden">
                <NavbarLoggedIn dark />
                <main className="flex-1 overflow-y-auto p-8 bg-gray-100">
                    {children}
                </main>
            </div>
        </div>
    )
}