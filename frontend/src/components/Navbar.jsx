import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <nav>
            <h1>Atlas</h1>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>   
        </nav>
    )
}

