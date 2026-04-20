import { Link } from 'react-router-dom'

export default function Footer() {
    return (
        <footer className="p-6 text-center border-t border-gray-200">
            <p className="font-conthrax text-2xl">Atlas</p>
            <p className="text-gray-400 text-sm mb-4">An Unscathed Project</p>
            <div className="flex gap-8 justify-center mb-4">
                <Link to="/privacy-policy" className="text-gray-500 hover:underline">Privacy Policy</Link>
                <Link to="/terms" className="text-gray-500 hover:underline">Terms</Link>
                <Link to="/documentation" className="text-gray-500 hover:underline">Documentation</Link>
            </div>
            <p className="text-gray-400 text-sm">© 2026 Unscathed. All rights reserved.</p>
        </footer>
    )
}