import { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft, ChevronRight } from "lucide-react";

const slides = [
  {
    id: 1,
    bg: "from-indigo-700 via-indigo-600 to-blue-500",
    eyebrow: "New Arrivals",
    headline: "Luxury Bags — Up to 30% Off",
    sub: "Exclusive designer collections at unbeatable prices. Limited stock available.",
    cta: "Shop Bags",
    to: "/products?category=Luxury%20Bags",
    badge: "🔥 Today Only",
  },
  {
    id: 2,
    bg: "from-amber-600 via-orange-500 to-yellow-400",
    eyebrow: "Flash Sale",
    headline: "Premium LV Sneakers — Limited Edition",
    sub: "Step into luxury. Authentic styles shipped directly from trusted suppliers.",
    cta: "Explore Shoes",
    to: "/products?category=Luxury%20Shoes",
    badge: "⚡ Flash Deal",
  },
  {
    id: 3,
    bg: "from-rose-600 via-pink-500 to-fuchsia-500",
    eyebrow: "Festive Season",
    headline: "Premium Perfumes — Upto 60% Off",
    sub: "Signature fragrances for every occasion.",
    cta: "Shop Perfumes",
    to: "/products?category=Perfumes",
    badge: "🎁 Special Offer",
  },
  {
    id: 4,
    bg: "from-emerald-600 via-teal-500 to-cyan-500",
    eyebrow: "Member Exclusive",
    headline: "Free Shipping on All Orders This Week",
    sub: "No minimum order. Shop the full collection and save on every purchase.",
    cta: "Browse All",
    to: "/products",
    badge: "🚀 Limited Time",
  },
];

const AUTO_INTERVAL = 4500;

export default function AdSlider() {
  const [current, setCurrent] = useState(0);
  const [paused, setPaused] = useState(false);

  const next = useCallback(() => {
    setCurrent((c) => (c + 1) % slides.length);
  }, []);

  const prev = useCallback(() => {
    setCurrent((c) => (c - 1 + slides.length) % slides.length);
  }, []);

  useEffect(() => {
    if (paused) return;
    const t = setInterval(next, AUTO_INTERVAL);
    return () => clearInterval(t);
  }, [paused, next]);

  const slide = slides[current];

  return (
    <section
      className="container-pad py-4"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      <div className="relative overflow-hidden rounded-2xl select-none">
        {/* Slide */}
        <div
          key={slide.id}
          className={`relative bg-gradient-to-r ${slide.bg} text-white px-8 py-10 md:px-14 md:py-14 transition-all duration-500`}
        >
          {/* Badge */}
          <span className="inline-block mb-3 text-xs font-bold uppercase tracking-wider bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
            {slide.badge}
          </span>

          <p className="text-sm font-medium text-white/80 uppercase tracking-widest mb-1">
            {slide.eyebrow}
          </p>
          <h2 className="text-2xl md:text-4xl font-extrabold leading-tight max-w-xl">
            {slide.headline}
          </h2>
          <p className="mt-3 text-white/85 text-sm md:text-base max-w-lg">
            {slide.sub}
          </p>

          <Link
            to={slide.to}
            className="inline-block mt-6 px-6 py-3 rounded-xl bg-white text-slate-900 font-semibold text-sm hover:scale-105 transition shadow-lg"
          >
            {slide.cta} →
          </Link>

          {/* Decorative circles */}
          <div className="absolute -right-10 -top-10 w-52 h-52 rounded-full bg-white/10 pointer-events-none" />
          <div className="absolute -right-4 bottom-[-40px] w-36 h-36 rounded-full bg-white/10 pointer-events-none" />
        </div>

        {/* Prev / Next arrows */}
        <button
          onClick={prev}
          aria-label="Previous slide"
          className="absolute left-3 top-1/2 -translate-y-1/2 h-9 w-9 rounded-full bg-black/30 hover:bg-black/50 text-white flex items-center justify-center backdrop-blur-sm transition"
        >
          <ChevronLeft size={20} />
        </button>
        <button
          onClick={next}
          aria-label="Next slide"
          className="absolute right-3 top-1/2 -translate-y-1/2 h-9 w-9 rounded-full bg-black/30 hover:bg-black/50 text-white flex items-center justify-center backdrop-blur-sm transition"
        >
          <ChevronRight size={20} />
        </button>
      </div>

      {/* Dots */}
      <div className="flex justify-center gap-2 mt-3">
        {slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            aria-label={`Go to slide ${i + 1}`}
            className={`h-2 rounded-full transition-all duration-300 ${
              i === current
                ? "w-6 bg-indigo-600 dark:bg-indigo-400"
                : "w-2 bg-slate-300 dark:bg-slate-600"
            }`}
          />
        ))}
      </div>
    </section>
  );
}
