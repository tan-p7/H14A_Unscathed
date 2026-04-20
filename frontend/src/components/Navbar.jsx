import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav className="flex justify-between items-center p-4 border-b border-gray-200 shadow-sm">
            <h1 className="text-4xl font-conthrax">Atlas</h1>
            <div className="flex gap-4 ">
                <Link to="/login" className="border border-gray-300 px-4 py-2 rounded-md hover:bg-gray-100">Login</Link>
                <Link to="/register" className="border border-gray-300 px-4 py-2 rounded-md hover:bg-gray-100">Register</Link>   
            </div>
        </nav>
    )
}

