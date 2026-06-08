import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchEventById } from '../services/api';
import { Calendar, MapPin, Users, Ticket, ArrowLeft } from 'lucide-react';

const EventDetail = () => {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setLoading(true);
    fetchEventById(id)
      .then(res => {
        setEvent(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="flex-grow flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="w-16 h-16 border-4 border-brand-200 border-t-brand-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 max-w-7xl mx-auto mt-10 text-center">
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 inline-block shadow-sm">
          Error loading event details: {error}
        </div>
        <div className="mt-4">
          <Link to="/events" className="text-brand-600 hover:underline">Back to Events</Link>
        </div>
      </div>
    );
  }

  if (!event) return null;

  return (
    <div className="pb-20">
      {/* Hero Section */}
      <div className="relative h-[60vh] min-h-[400px] w-full">
        <div className="absolute inset-0">
          <img src="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1000&q=80" alt={event.title} className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/60 to-transparent"></div>
        </div>
        
        <div className="absolute inset-0 flex flex-col justify-end max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
          <Link to="/events" className="text-slate-300 hover:text-white flex items-center gap-2 w-fit mb-6 transition-colors animate-fade-in">
            <ArrowLeft className="w-4 h-4" />
            Back to events
          </Link>
          
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 animate-slide-up">
            <div className="max-w-3xl">
              <div className="flex gap-3 mb-4">
                <span className="bg-brand-500/20 text-brand-300 backdrop-blur-sm border border-brand-500/30 px-3 py-1 rounded-full text-sm font-semibold">
                  Event
                </span>
                <span className="bg-white/10 text-white backdrop-blur-sm border border-white/20 px-3 py-1 rounded-full text-sm">
                  {event.current_attendees || 0} / {event.max_attendees || 'Unlimited'} Attending
                </span>
              </div>
              <h1 className="text-4xl md:text-6xl font-extrabold text-white mb-4 tracking-tight leading-tight">
                {event.title}
              </h1>
              <div className="flex flex-wrap gap-4 text-slate-200">
                <div className="flex items-center gap-2"><Calendar className="w-5 h-5 text-brand-400" /> {new Date(event.start_date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</div>
                <div className="flex items-center gap-2"><MapPin className="w-5 h-5 text-brand-400" /> {event.location || 'TBD'}</div>
              </div>
            </div>
            
            <Link 
              to={`/events/${event.id}/register`}
              className="bg-brand-500 hover:bg-brand-600 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(14,165,233,0.4)] transition-all hover:scale-105 flex items-center justify-center gap-2"
            >
              <Ticket className="w-6 h-6" />
              Register Now
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-12">
          {/* Overview */}
          <section className="bg-white dark:bg-dark-card rounded-3xl p-8 animate-slide-up border border-slate-200 dark:border-dark-border">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Overview</h2>
            <p className="text-slate-600 dark:text-slate-400 text-lg leading-relaxed">
              {event.description || 'No description available for this event.'}
            </p>
          </section>

          {/* Event Info */}
          <section className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-8">Event Information</h2>
            <div className="bg-white dark:bg-dark-card rounded-2xl p-6 border border-slate-200 dark:border-dark-border">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Start Date</p>
                  <p className="text-lg font-bold text-slate-900 dark:text-white mt-2">
                    {new Date(event.start_date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">End Date</p>
                  <p className="text-lg font-bold text-slate-900 dark:text-white mt-2">
                    {new Date(event.end_date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Location</p>
                  <p className="text-lg font-bold text-slate-900 dark:text-white mt-2">{event.location || 'TBD'}</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Capacity</p>
                  <p className="text-lg font-bold text-slate-900 dark:text-white mt-2">{event.max_attendees || 'Unlimited'}</p>
                </div>
              </div>
            </div>
          </section>
        </div>

        {/* Sidebar: Quick Info */}
        <div className="space-y-8 animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <div className="bg-white dark:bg-dark-card rounded-3xl p-8 sticky top-24 border border-slate-200 dark:border-dark-border">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
              <Users className="w-6 h-6 text-brand-500" />
              Quick Stats
            </h2>
            
            <div className="space-y-6">
              <div>
                <p className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Registered</p>
                <p className="text-3xl font-bold text-brand-600 dark:text-brand-400 mt-2">{event.current_attendees || 0}</p>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Total Capacity</p>
                <p className="text-3xl font-bold text-slate-900 dark:text-white mt-2">{event.max_attendees || 'Unlimited'}</p>
              </div>
              <div className="pt-6 border-t border-slate-200 dark:border-dark-border">
                <p className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Status</p>
                <div className="mt-3">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold ${
                    event.is_active 
                      ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' 
                      : 'bg-slate-100 dark:bg-slate-900/30 text-slate-700 dark:text-slate-400'
                  }`}>
                    {event.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventDetail;
