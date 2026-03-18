import { Helmet } from "react-helmet-async";

export default function Contact() {
  return (
    <section className="container-pad py-10">
      <Helmet><title>GOLD | Contact</title></Helmet>
      <h1 className="text-3xl font-bold mb-4">Contact</h1>
      <form className="max-w-xl space-y-3">
        <input className="w-full p-3 rounded-lg border dark:bg-slate-900" placeholder="Your Name" />
        <input className="w-full p-3 rounded-lg border dark:bg-slate-900" placeholder="Your Email" />
        <textarea className="w-full p-3 rounded-lg border dark:bg-slate-900" rows="5" placeholder="Message" />
        <button type="button" className="px-5 py-3 rounded-lg bg-slate-900 text-white dark:bg-white dark:text-slate-900">
          Send Message
        </button>
      </form>
    </section>
  );
}