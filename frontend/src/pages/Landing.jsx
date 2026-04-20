import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Link } from "react-router-dom";

export default function Landing() {
    return (
        <div>   
            <Navbar />  
            <section className="flex flex-col items-center px-8 py-20">
                <h1 className="text-5xl font-bold max-w-3xl">Switch to Atlas. Save time. Supply Chain Management Simplified.</h1>
                <p className="max-w-xl mt-4 text-gray-500">With Atlas, you can easily track your inventory levels, manage your orders, and ship your products to your customers. All while being compliant with industry regulations.</p>
                <div className="flex gap-4 mt-8"> 
                    <Link to="/register">
                        <button className="bg-deep-sky-blue-600 text-white px-6 py-3 rounded-lg">Get Started</button>
                    </Link>
                    <Link to="/dashboard">
                        <button className="bg-gray-100 text-gray-800 px-6 py-3 rounded-lg">Learn More</button>
                    </Link>
                </div>
            </section>

            
            <section className="flex justify-center gap-8 bg-gray-50 py-16">
                <div>
                    <p className="text-4xl font-bold">10M+</p>
                    <p className="text-gray-500 text-sm mt-1">Orders fulfilled</p>
                </div>
                <div>
                    <p className="text-4xl font-bold">500+</p>
                    <p className="text-gray-500 text-sm mt-1">Businesses Trust Us</p>
                </div>
                <div>
                    <p className="text-4xl font-bold">98%</p>
                    <p className="text-gray-500 text-sm mt-1">Compliance Rate</p>
                </div>
            </section>
            <Footer />
        </div>
    )
}