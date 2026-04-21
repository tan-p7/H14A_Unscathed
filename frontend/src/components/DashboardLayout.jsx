import Sidebar from './Sidebar'
import NavbarLoggedIn from './NavbarLoggedIn'

export default function DashboardLayout({ children }) {
    return (
        <div className="flex h-screen">
            <Sidebar />
            <div className="flex flex-col flex-1 overflow-hidden">
                <NavbarLoggedIn />
                <main className="flex-1 overflow-y-auto p-8 bg-white">
                    {children}
                </main>
            </div>
        </div>
    )
}