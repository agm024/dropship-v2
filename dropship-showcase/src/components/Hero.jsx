import { motion } from "framer-motion";
import { Link } from "react-router-dom";

export default function Hero() {
  return (
    <section className="container-pad py-12 md:py-20">
      <motion.div
        initial={{ opacity: 0, y: 25 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="rounded-3xl p-8 md:p-14 bg-gradient-to-br from-indigo-600 via-blue-600 to-cyan-500 text-white"
      >
        <h1 className="text-3xl md:text-5xl font-bold leading-tight">Discover Trending Dropshipping Products</h1>
        <p className="mt-4 max-w-2xl text-white/90">
          Browse curated products and jump directly to trusted supplier pages using Buy Now.
        </p>
        <Link to="/products" className="inline-block mt-6 px-5 py-3 rounded-xl bg-white text-slate-900 font-semibold hover:scale-105 transition">
          Explore Products
        </Link>
      </motion.div>
    </section>
  );
}