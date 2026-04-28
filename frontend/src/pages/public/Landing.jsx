import Navbar from "../../components/shared/Navbar";
import Footer from "../../components/shared/Footer";
import { Link } from "react-router-dom";
import { useState } from "react";

export default function Landing() {
    const [showBanner, setShowBanner] = useState(true)

    return (
        <div className="min-h-screen flex flex-col">
            <Navbar />

            {/* Promo banner */}
            {showBanner && (
                <div className="bg-deep-sky-blue-600 py-3 px-6 flex items-center justify-between gap-4">
                    <div className="flex-1" />
                    <div className="flex items-center gap-4 flex-1 justify-center flex-wrap">
                        <p className="text-white text-sm font-semibold">
                            Get 90% off your plan for your first 3 months when you buy by 30 April.
                        </p>
                        <Link to="/register">
                            <button className="bg-white text-deep-sky-blue-600 text-sm font-semibold px-4 py-1.5 rounded-lg hover:bg-deep-sky-blue-50 transition-colors whitespace-nowrap">
                                Claim offer →
                            </button>
                        </Link>
                    </div>
                    <div className="flex-1 flex justify-end">
                        <button
                            onClick={() => setShowBanner(false)}
                            className="text-white hover:text-deep-sky-blue-100 text-lg leading-none"
                            aria-label="Dismiss banner"
                        >
                            ✕
                        </button>
                    </div>
                </div>
            )}

            {/* Hero */}
            <section className="flex flex-col items-center text-center px-6 py-8 bg-white">
                <div className="inline-block bg-deep-sky-blue-50 text-deep-sky-blue-600 text-xs font-semibold px-3 py-1 rounded-full mb-6">
                    Now with multi-country e-invoicing compliance
                </div>
                <h1 className="text-5xl font-bold text-gray-900 max-w-3xl leading-tight mb-4">
                    Supply chain management simplified.
                </h1>
                <p className="text-gray-500 max-w-xl text-lg mb-8">
                    Generate despatch advices, create compliant e-invoices, and manage your orders, all in one place.
                </p>
                <div className="flex flex-col items-center gap-4">
                    <div className="flex gap-3">
                        <Link to="/register">
                            <button className="bg-deep-sky-blue-600 text-white px-6 py-3 rounded-lg hover:bg-deep-sky-blue-700 font-medium">
                                Start for free
                            </button>
                        </Link>
                        <Link to="/pricing">
                            <button className="border border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-50 font-medium">
                                View pricing
                            </button>
                        </Link>
                    </div>
                    <p className="text-gray-400 text-sm">No credit card required. Free plan available.</p>
                </div>
            </section>

            {/* Stats */}
            <section className="bg-gray-50 py-16 px-6">
                <div className="max-w-4xl mx-auto flex justify-center gap-16">
                    <div className="text-center">
                        <p className="text-4xl font-bold text-gray-900">10M+</p>
                        <p className="text-gray-500 text-sm mt-1">Orders fulfilled</p>
                    </div>
                    <div className="text-center">
                        <p className="text-4xl font-bold text-gray-900">500+</p>
                        <p className="text-gray-500 text-sm mt-1">Businesses trust Atlas</p>
                    </div>
                    <div className="text-center">
                        <p className="text-4xl font-bold text-gray-900">98%</p>
                        <p className="text-gray-500 text-sm mt-1">Compliance rate</p>
                    </div>
                    <div className="text-center">
                        <p className="text-4xl font-bold text-gray-900">5</p>
                        <p className="text-gray-500 text-sm mt-1">Countries supported</p>
                    </div>
                </div>
            </section>

            {/* Features */}
            <section className="py-20 px-6 bg-white">
                <div className="max-w-5xl mx-auto">
                    <h2 className="text-3xl font-bold text-gray-900 text-center mb-4">Everything you need to run your supply chain</h2>
                    <p className="text-gray-500 text-center mb-12">Built around the UBL 2.1 standard so your documents work with any trading partner.</p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="p-6 border border-gray-100 rounded-xl" style={{ backgroundColor: '#e5f8ff' }}>
                            <div className="text-2xl mb-3">📦</div>
                            <h3 className="font-semibold text-gray-800 mb-2">Order Management</h3>
                            <p className="text-gray-500 text-sm">Create and track purchase orders from placement through to delivery.</p>
                        </div>
                        <div className="p-6 border border-gray-100 rounded-xl" style={{ backgroundColor: '#e5f8ff' }}>
                            <div className="text-2xl mb-3">🚚</div>
                            <h3 className="font-semibold text-gray-800 mb-2">Despatch Advice</h3>
                            <p className="text-gray-500 text-sm">Generate UBL 2.1 compliant despatch advice documents with a few clicks.</p>
                        </div>
                        <div className="p-6 border border-gray-100 rounded-xl" style={{ backgroundColor: '#e5f8ff' }}>
                            <div className="text-2xl mb-3">🧾</div>
                            <h3 className="font-semibold text-gray-800 mb-2">E-Invoicing</h3>
                            <p className="text-gray-500 text-sm">Generate compliant invoices for AU/NZ, Singapore, Japan, EU, and the US.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="bg-gray-50 py-20 px-6">
                <div className="max-w-2xl mx-auto text-center">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">Start using Atlas for free</h2>
                    <p className="text-gray-500 mb-8">Access all core features for free. Upgrade when you're ready.</p>
                    <div className="flex flex-col sm:flex-row gap-3 justify-center items-center max-w-md mx-auto">
                        <input
                            type="email"
                            placeholder="Enter your email"
                            className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-deep-sky-blue-400"
                        />
                        <Link to="/register">
                            <button className="w-full sm:w-auto bg-deep-sky-blue-600 text-white px-6 py-3 rounded-lg hover:bg-deep-sky-blue-700 text-sm font-medium whitespace-nowrap">
                                Start free trial
                            </button>
                        </Link>
                    </div>
                    <p className="text-gray-400 text-xs mt-3">30-day free trial. No credit card required.</p>
                </div>
            </section>

            <Footer />
        </div>
    )
}