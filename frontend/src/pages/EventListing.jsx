import React, { useState, useEffect } from 'react';
import { fetchEvents } from '../services/api';
import { Calendar, MapPin, Users, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const EventListing = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchEvents()
      .then(res => {
        setEvents(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

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
          Error loading events: {error}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-12 text-center animate-slide-up">
        <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 mb-4 tracking-tight">Upcoming Events</h1>
        <p className="text-lg text-slate-500 max-w-2xl mx-auto">Discover and register for the most exciting conferences, workshops, and meetups happening around the globe.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {events.map((event, index) => (
          <div 
            key={event.id} 
            className="glass rounded-3xl overflow-hidden hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 group animate-fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="relative h-56 bg-slate-200 overflow-hidden">
              <img 
                src={event.image} 
                alt={event.title} 
                className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                onError={(e) => { e.target.onerror = null; e.target.src = 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1000&q=80'; }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/20 to-transparent z-10 pointer-events-none"></div>
              <div className="absolute bottom-4 left-4 z-20">
                <div className="bg-brand-500 text-white text-xs font-bold px-3 py-1 rounded-full mb-2 inline-block shadow-lg border border-brand-400">
                  {new Date(event.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </div>
              </div>
            </div>
            
            <div className="p-6">
              <h3 className="text-xl font-bold text-slate-900 mb-3 line-clamp-2">{event.title}</h3>
              
              <div className="space-y-2 mb-6">
                <div className="flex items-center text-slate-500 text-sm">
                  <MapPin className="w-4 h-4 mr-2 text-brand-500" />
                  {event.location}
                </div>
                <div className="flex items-center text-slate-500 text-sm">
                  <Users className="w-4 h-4 mr-2 text-brand-500" />
                  {event.registered} / {event.capacity} Attending
                </div>
              </div>
              
              <div className="pt-4 border-t border-slate-100 flex justify-between items-center">
                <div className="w-full bg-slate-100 rounded-full h-2 mr-4 overflow-hidden">
                  <div 
                    className="bg-brand-500 h-2 rounded-full" 
                    style={{ width: `${event.capacity > 0 ? Math.min((event.registered / event.capacity) * 100, 100) : 0}%` }}
                  ></div>
                </div>
                <Link 
                  to={`/events/${event.id}`}
                  className="bg-slate-900 hover:bg-brand-600 text-white p-2 rounded-full transition-colors flex-shrink-0"
                >
                  <ArrowRight className="w-5 h-5" />
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventListing;
