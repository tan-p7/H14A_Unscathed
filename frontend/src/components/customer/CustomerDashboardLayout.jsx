import CustomerSidebar from './CustomerSidebar'
import NavbarLoggedIn from '../shared/NavbarLoggedIn'

export default function CustomerDashboardLayout({ children }) {
    return (
        <div className="flex h-screen">
            <CustomerSidebar />
            <div className="flex flex-col flex-1 overflow-hidden">
                <NavbarLoggedIn />
            <main className="flex-1 overflow-y-auto p-8 bg-gray-100">                    {children}
                </main>
            </div>
        </div>
    )
}