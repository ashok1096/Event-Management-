import { Link } from 'react-router-dom';
import { CalendarDays, Users, Star, ArrowRight } from 'lucide-react';

const Home = () => {
  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)]">
      {/* Hero Section */}
      <section className="relative flex-grow flex items-center justify-center overflow-hidden bg-slate-900 py-20">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1492684223066-81342ee5ff30?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80')] bg-cover bg-center opacity-30"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-slate-900/80 to-slate-900"></div>
        
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center animate-slide-up">
          <div className="inline-block bg-brand-500/20 border border-brand-500/30 backdrop-blur-md px-4 py-1.5 rounded-full text-brand-300 font-semibold mb-6">
            The Ultimate Event Experience
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight mb-6">
            Manage events with <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-emerald-400">precision</span>
          </h1>
          <p className="mt-4 max-w-2xl text-xl text-slate-300 mx-auto mb-10">
            Event Pulse provides a seamless, dynamic, and premium platform for organizers and attendees. Discover conferences, register easily, and manage everything in realtime.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link 
              to="/events" 
              className="bg-brand-500 hover:bg-brand-600 text-white px-8 py-4 rounded-full font-bold text-lg transition-all shadow-lg shadow-brand-500/30 hover:shadow-brand-500/50 flex items-center justify-center gap-2 hover:-translate-y-1"
            >
              Browse Events <ArrowRight className="w-5 h-5" />
            </Link>
            <Link 
              to="/register" 
              className="bg-white/10 hover:bg-white/20 text-white backdrop-blur-md border border-white/20 px-8 py-4 rounded-full font-bold text-lg transition-all flex items-center justify-center gap-2 hover:-translate-y-1"
            >
              Create an Account
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">Why choose Event Pulse?</h2>
            <p className="text-lg text-slate-500 max-w-2xl mx-auto">Everything you need to host, manage, and attend world-class events in one seamless platform.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="glass rounded-3xl p-8 hover:-translate-y-2 transition-all duration-300 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="w-14 h-14 bg-brand-100 rounded-2xl flex items-center justify-center mb-6">
                <CalendarDays className="w-7 h-7 text-brand-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Dynamic Scheduling</h3>
              <p className="text-slate-600">Explore fully responsive, multi-track session schedules with up-to-the-minute changes seamlessly synced.</p>
            </div>
            
            <div className="glass rounded-3xl p-8 hover:-translate-y-2 transition-all duration-300 animate-slide-up" style={{ animationDelay: '0.3s' }}>
              <div className="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center mb-6">
                <Users className="w-7 h-7 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Realtime Dashboard</h3>
              <p className="text-slate-600">Organizers get a bird's-eye view of check-ins, registrations, and engagement through our dynamic dashboard.</p>
            </div>

            <div className="glass rounded-3xl p-8 hover:-translate-y-2 transition-all duration-300 animate-slide-up" style={{ animationDelay: '0.4s' }}>
              <div className="w-14 h-14 bg-amber-100 rounded-2xl flex items-center justify-center mb-6">
                <Star className="w-7 h-7 text-amber-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Instant Feedback</h3>
              <p className="text-slate-600">Gather session ratings and reviews from attendees instantly to measure success and improve future events.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
