import Sidebar from './Sidebar'

export default function DashboardLayout({ children }) {
    return (
        <div className="flex h-screen">
            <Sidebar />
            <main className="flex-1 overflow-hidden p-8 bg-white h-full">
                {children}
            </main>
        </div>
    )
}