import Navbar from "../components/Navbar";
import { Link } from "react-router-dom";

export default function Landing() {
    return (
        <div>   
            <Navbar />  
            <section>
                <h1>Switch to Atlas. Save time. Supply Chain Management Simplified.</h1>
                <p>With Atlas, you can easily track your inventory levels, manage your orders, and ship your products to your customers. All while being compliant with industry regulations.</p>
                <Link to="/register">
                    <button >Get Started</button>
                </Link>
                <Link to="/dashboard">
                    <button>Learn More</button>
                </Link>
            </section>
        </div>


    )
}