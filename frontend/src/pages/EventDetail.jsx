import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchEventById } from '../services/api';
import { Calendar, MapPin, Clock, Users, Ticket, ArrowLeft } from 'lucide-react';

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
          <img src={event.image} alt={event.title} className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-dark-900 via-dark-900/60 to-transparent"></div>
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
                  Conference
                </span>
                <span className="bg-white/10 text-white backdrop-blur-sm border border-white/20 px-3 py-1 rounded-full text-sm">
                  {event.registered} / {event.capacity} Filled
                </span>
              </div>
              <h1 className="text-4xl md:text-6xl font-extrabold text-white mb-4 tracking-tight leading-tight">
                {event.title}
              </h1>
              <div className="flex flex-wrap gap-4 text-slate-200">
                <div className="flex items-center gap-2"><Calendar className="w-5 h-5 text-brand-400" /> {new Date(event.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</div>
                <div className="flex items-center gap-2"><Clock className="w-5 h-5 text-brand-400" /> {event.time}</div>
                <div className="flex items-center gap-2"><MapPin className="w-5 h-5 text-brand-400" /> {event.location}</div>
              </div>
            </div>
            
            <Link 
              to={`/events/${event.id}/register`}
              className="bg-brand-500 hover:bg-brand-600 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(20,184,166,0.4)] transition-all hover:scale-105 flex items-center justify-center gap-2"
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
          <section className="glass rounded-3xl p-8 animate-slide-up">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">Overview</h2>
            <p className="text-slate-600 text-lg leading-relaxed">
              {event.description}
            </p>
          </section>

          {/* Schedule */}
          <section className="animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <h2 className="text-3xl font-bold text-slate-900 mb-8">Schedule</h2>
            <div className="space-y-4">
              {event.sessions && event.sessions.length > 0 ? (
                event.sessions.map((session, idx) => (
                  <div key={session.id} className="glass rounded-2xl p-6 flex flex-col sm:flex-row gap-6 items-start sm:items-center hover:border-brand-300 transition-colors">
                    <div className="bg-brand-50 text-brand-600 font-bold px-4 py-2 rounded-lg min-w-[120px] text-center">
                      {session.time}
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-slate-800 mb-1">{session.title}</h3>
                      <p className="text-slate-500">by <span className="font-medium text-slate-700">{session.speaker}</span></p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 italic">Schedule will be announced soon.</p>
              )}
            </div>
          </section>
        </div>

        {/* Sidebar: Speakers */}
        <div className="space-y-8 animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <div className="glass rounded-3xl p-8 sticky top-24">
            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
              <Users className="w-6 h-6 text-brand-500" />
              Speakers
            </h2>
            
            <div className="space-y-6">
              {event.speakers && event.speakers.length > 0 ? (
                event.speakers.map(speaker => (
                  <div key={speaker.id} className="flex items-center gap-4 group">
                    <img src={speaker.avatar} alt={speaker.name} className="w-16 h-16 rounded-full object-cover border-2 border-transparent group-hover:border-brand-500 transition-all" />
                    <div>
                      <h4 className="font-bold text-slate-900 group-hover:text-brand-600 transition-colors">{speaker.name}</h4>
                      <p className="text-sm text-slate-500">{speaker.role}</p>
                      <p className="text-xs text-brand-500 font-medium">{speaker.company}</p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 italic">Speakers will be announced soon.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventDetail;
