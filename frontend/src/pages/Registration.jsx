import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { fetchEventById, registerForEvent } from '../services/api';
import { CheckCircle2, ArrowLeft, Ticket } from 'lucide-react';

const Registration = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [ticketId, setTicketId] = useState('');
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    ticketType: 'general'
  });

  useEffect(() => {
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    registerForEvent(id, formData)
      .then(res => {
        setSuccess(true);
        setTicketId(res.ticketId);
      })
      .catch(err => {
        setError(err.message || 'Registration failed');
      })
      .finally(() => {
        setSubmitting(false);
      });
  };

  if (loading) {
    return (
      <div className="flex-grow flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="w-16 h-16 border-4 border-brand-200 border-t-brand-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error && !event) {
    return (
      <div className="p-8 max-w-2xl mx-auto mt-10 text-center">
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 inline-block shadow-sm">
          {error}
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center animate-fade-in">
        <div className="glass rounded-3xl p-12 flex flex-col items-center">
          <div className="w-24 h-24 bg-emerald-100 rounded-full flex items-center justify-center mb-6">
            <CheckCircle2 className="w-12 h-12 text-emerald-500" />
          </div>
          <h1 className="text-4xl font-extrabold text-slate-900 mb-4">You're In!</h1>
          <p className="text-lg text-slate-600 mb-8">
            You've successfully registered for <span className="font-bold text-slate-800">{event?.title}</span>. 
            A confirmation email has been sent.
          </p>
          <div className="bg-slate-50 border border-slate-200 border-dashed rounded-xl p-6 mb-8 w-full max-w-sm">
            <p className="text-slate-500 text-sm uppercase tracking-wide font-semibold mb-1">Your Ticket ID</p>
            <p className="text-2xl font-mono font-bold text-brand-600">{ticketId}</p>
          </div>
          <Link to="/" className="bg-slate-900 text-white hover:bg-slate-800 px-8 py-3 rounded-full font-medium transition-colors">
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-12 animate-slide-up">
      <Link to={`/events/${id}`} className="text-slate-500 hover:text-brand-600 flex items-center gap-2 mb-8 transition-colors w-fit">
        <ArrowLeft className="w-4 h-4" />
        Back to Event Details
      </Link>

      <div className="glass rounded-3xl p-8 md:p-12">
        <div className="mb-10 text-center">
          <h1 className="text-3xl font-extrabold text-slate-900 mb-2">Secure Your Spot</h1>
          <p className="text-slate-500">Registering for: <span className="font-semibold text-slate-700">{event?.title}</span></p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">First Name *</label>
              <input 
                type="text" 
                name="firstName" 
                required 
                value={formData.firstName} 
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all bg-slate-50 hover:bg-white focus:bg-white"
                placeholder="Jane"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Last Name *</label>
              <input 
                type="text" 
                name="lastName" 
                required 
                value={formData.lastName} 
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all bg-slate-50 hover:bg-white focus:bg-white"
                placeholder="Doe"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Email Address *</label>
            <input 
              type="email" 
              name="email" 
              required 
              value={formData.email} 
              onChange={handleInputChange}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all bg-slate-50 hover:bg-white focus:bg-white"
              placeholder="jane@company.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Company / Organization</label>
            <input 
              type="text" 
              name="company" 
              value={formData.company} 
              onChange={handleInputChange}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all bg-slate-50 hover:bg-white focus:bg-white"
              placeholder="Optional"
            />
          </div>

          <div className="pt-4">
            <label className="block text-sm font-bold text-slate-900 mb-4">Select Ticket Type</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <label className={`relative flex cursor-pointer rounded-2xl border p-4 shadow-sm focus:outline-none transition-all ${formData.ticketType === 'general' ? 'border-brand-500 bg-brand-50/50 ring-1 ring-brand-500' : 'border-slate-200 bg-white hover:bg-slate-50'}`}>
                <input type="radio" name="ticketType" value="general" checked={formData.ticketType === 'general'} onChange={handleInputChange} className="sr-only" />
                <span className="flex flex-1">
                  <span className="flex flex-col">
                    <span className="block text-sm font-bold text-slate-900">General Admission</span>
                    <span className="mt-1 flex items-center text-sm text-slate-500">Access to all standard sessions.</span>
                  </span>
                </span>
                <CheckCircle2 className={`h-5 w-5 ${formData.ticketType === 'general' ? 'text-brand-500' : 'text-transparent'}`} />
              </label>

              <label className={`relative flex cursor-pointer rounded-2xl border p-4 shadow-sm focus:outline-none transition-all ${formData.ticketType === 'vip' ? 'border-brand-500 bg-brand-50/50 ring-1 ring-brand-500' : 'border-slate-200 bg-white hover:bg-slate-50'}`}>
                <input type="radio" name="ticketType" value="vip" checked={formData.ticketType === 'vip'} onChange={handleInputChange} className="sr-only" />
                <span className="flex flex-1">
                  <span className="flex flex-col">
                    <span className="block text-sm font-bold text-slate-900">VIP Pass ($299)</span>
                    <span className="mt-1 flex items-center text-sm text-slate-500">Front row, exclusive lounge.</span>
                  </span>
                </span>
                <CheckCircle2 className={`h-5 w-5 ${formData.ticketType === 'vip' ? 'text-brand-500' : 'text-transparent'}`} />
              </label>
            </div>
          </div>

          <div className="pt-8 mt-8 border-t border-slate-100">
            <button 
              type="submit" 
              disabled={submitting}
              className="w-full bg-brand-500 hover:bg-brand-600 text-white py-4 rounded-xl font-bold text-lg transition-all flex justify-center items-center gap-2 shadow-lg shadow-brand-500/30 hover:shadow-brand-500/50 disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Processing...
                </>
              ) : (
                <>
                  <Ticket className="w-5 h-5" />
                  Complete Registration
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Registration;
