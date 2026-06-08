import { useState, useEffect } from 'react';
import * as api from '../services/api';
import { Calendar, Users, Mic, UserCheck, MessageSquare, ClipboardCheck, Trash2, Plus, X, Play, Square, Search, RefreshCw, Edit2, Check } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

// ── Modal ──
const Modal = ({ title, onClose, children }) => (
  <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in p-4" onClick={onClose}>
    <div className="bg-white dark:bg-dark-card rounded-2xl shadow-2xl border border-slate-200 dark:border-dark-border w-full max-w-lg max-h-[90vh] overflow-y-auto animate-scale-in" onClick={e => e.stopPropagation()}>
      <div className="flex justify-between items-center p-6 border-b border-slate-200 dark:border-dark-border sticky top-0 bg-white/90 dark:bg-dark-card/90 backdrop-blur z-10">
        <h3 className="text-xl font-bold text-slate-900 dark:text-white">{title}</h3>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 bg-slate-100 hover:bg-slate-200 dark:bg-dark-bg dark:hover:bg-slate-700 p-2 rounded-full transition-colors"><X className="w-5 h-5" /></button>
      </div>
      <div className="p-6">{children}</div>
    </div>
  </div>
);

// ── Form Input ──
const FormInput = ({ label, type = 'text', value, onChange, required, placeholder }) => (
  <div className="mb-4">
    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1.5">{label}</label>
    {type === 'textarea' ? (
      <textarea value={value} onChange={onChange} required={required} placeholder={placeholder}
        className="w-full px-4 py-2.5 bg-slate-50 dark:bg-dark-bg border border-slate-300 dark:border-dark-border rounded-xl outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-900 dark:text-white text-sm transition-all" rows={3} />
    ) : (
      <input type={type} value={value} onChange={onChange} required={required} placeholder={placeholder}
        className="w-full px-4 py-2.5 bg-slate-50 dark:bg-dark-bg border border-slate-300 dark:border-dark-border rounded-xl outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-900 dark:text-white text-sm transition-all" />
    )}
  </div>
);

// ── Status Badge ──
const Badge = ({ text, color = 'slate' }) => {
  const colors = { 
    green: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-500/30', 
    red: 'bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400 border border-red-200 dark:border-red-500/30', 
    blue: 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400 border border-blue-200 dark:border-blue-500/30', 
    amber: 'bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-400 border border-amber-200 dark:border-amber-500/30', 
    slate: 'bg-slate-100 text-slate-700 dark:bg-slate-500/20 dark:text-slate-400 border border-slate-200 dark:border-slate-500/30', 
    brand: 'bg-brand-100 text-brand-700 dark:bg-brand-500/20 dark:text-brand-400 border border-brand-200 dark:border-brand-500/30' 
  };
  return <span className={`px-2.5 py-1 rounded-md text-[11px] font-bold uppercase tracking-wider ${colors[color] || colors.slate}`}>{text}</span>;
};

const statusColor = (s) => {
  if (!s) return 'slate';
  const l = s.toLowerCase();
  if (['upcoming','scheduled','registered','pending'].includes(l)) return 'blue';
  if (['ongoing','checked_in','completed_pay'].includes(l)) return 'amber';
  if (['completed','confirmed'].includes(l)) return 'green';
  if (['cancelled','failed'].includes(l)) return 'red';
  return 'slate';
};

const Dashboard = () => {
  const { user } = useAuth();
  const [tab, setTab] = useState('events');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const [editId, setEditId] = useState(null);
  const [saving, setSaving] = useState(false);
  
  const [searchId, setSearchId] = useState('');
  const [counts, setCounts] = useState({});

  const tabs = [
    { id: 'events', label: 'Events', icon: Calendar },
    { id: 'registrations', label: 'Registrations', icon: Users },
    { id: 'sessions', label: 'Sessions', icon: ClipboardCheck },
    { id: 'speakers', label: 'Speakers', icon: Mic },
    { id: 'checkins', label: 'Check-ins', icon: UserCheck },
    { id: 'feedback', label: 'Feedback', icon: MessageSquare },
  ];

  const fetchData = async () => {
    setLoading(true); setError('');
    try {
      let res;
      switch (tab) {
        case 'events': res = await api.getEvents(); setData(Array.isArray(res) ? res : []); break;
        case 'registrations': {
          const events = await api.getEvents();
          let allRegs = [];
          for (const ev of (Array.isArray(events) ? events : [])) {
            try { const r = await api.getRegistrationsByEvent(ev.id); allRegs = allRegs.concat(r); } catch { /* skip on error */ }
          }
          setData(allRegs); break;
        }
        case 'sessions': { const r = await api.getSessions(); setData(r?.sessions || []); break; }
        case 'speakers': res = await api.getSpeakers(); setData(Array.isArray(res) ? res : []); break;
        case 'feedback': { const r = await api.getFeedbacks(); setData(r?.feedbacks || []); break; }
        case 'checkins': setData([]); break;
        default: setData([]);
      }
    } catch (err) { setError(err.message); setData([]); }
    setLoading(false);
  };

  const fetchCounts = async () => {
    try {
      const [ev, sess, sp, fb] = await Promise.allSettled([
        api.getEvents(), api.getSessions(), api.getSpeakers(), api.getFeedbacks()
      ]);
      setCounts({
        events: ev.status === 'fulfilled' ? (Array.isArray(ev.value) ? ev.value.length : 0) : 0,
        sessions: sess.status === 'fulfilled' ? (sess.value?.total || 0) : 0,
        speakers: sp.status === 'fulfilled' ? (Array.isArray(sp.value) ? sp.value.length : 0) : 0,
        feedback: fb.status === 'fulfilled' ? (fb.value?.total || 0) : 0,
      });
    } catch { /* ignore count fetch errors */ }
  };

  useEffect(() => { fetchData(); }, [tab]);
  useEffect(() => { fetchCounts(); }, []);

  // ── CRUD handlers ──
  const handleDelete = async (id) => {
    if (!window.confirm('Delete this record permanently?')) return;
    try {
      if (tab === 'events') await api.deleteEvent(id);
      else if (tab === 'sessions') await api.deleteSession(id);
      else if (tab === 'speakers') await api.deleteSpeaker(id);
      else if (tab === 'feedback') await api.deleteFeedback(id);
      fetchData(); fetchCounts();
      alert('Delete successful!');
    } catch (e) { alert('Delete failed: ' + e.message); }
  };

  const openCreateModal = () => {
    setForm({});
    setIsEditing(false);
    setEditId(null);
    setModalOpen(true);
  };

  const openEditModal = (item) => {
    // Format dates for input type="datetime-local" if they exist
    const formattedItem = { ...item };
    ['start_date', 'end_date', 'start_time', 'end_time'].forEach(field => {
      if (formattedItem[field]) {
        formattedItem[field] = new Date(formattedItem[field]).toISOString().slice(0, 16);
      }
    });
    setForm(formattedItem);
    setEditId(item.id || item._id);
    setIsEditing(true);
    setModalOpen(true);
  };

  const handleSave = async (e) => {
    e.preventDefault(); setSaving(true);
    try {
      let payload = { ...form };
      
      // Formatting payload for backend
      if (tab === 'events') {
        payload.start_date = new Date(payload.start_date).toISOString();
        payload.end_date = new Date(payload.end_date).toISOString();
        payload.max_attendees = parseInt(payload.max_attendees) || null;
      } else if (tab === 'registrations') {
        payload.event_id = parseInt(payload.event_id);
      } else if (tab === 'sessions') {
        payload.event_id = parseInt(payload.event_id);
        payload.speaker_id = payload.speaker_id ? parseInt(payload.speaker_id) : null;
        payload.start_time = new Date(payload.start_time).toISOString();
        payload.end_time = new Date(payload.end_time).toISOString();
        payload.capacity = parseInt(payload.capacity) || null;
      } else if (tab === 'feedback') {
        payload.event_id = payload.event_id ? parseInt(payload.event_id) : null;
        payload.session_id = payload.session_id ? parseInt(payload.session_id) : null;
        payload.registration_id = payload.registration_id ? parseInt(payload.registration_id) : null;
        payload.rating = parseInt(payload.rating);
      }

      if (isEditing) {
        if (tab === 'events') await api.updateEvent(editId, payload);
        else if (tab === 'registrations') await api.updateRegistration(editId, payload);
        else if (tab === 'sessions') await api.updateSession(editId, payload);
        else if (tab === 'speakers') await api.updateSpeaker(editId, payload);
        else if (tab === 'feedback') await api.updateFeedback(editId, payload);
      } else {
        if (tab === 'events') await api.createEvent(payload);
        else if (tab === 'registrations') await api.createRegistration(payload);
        else if (tab === 'sessions') await api.createSession(payload);
        else if (tab === 'speakers') await api.createSpeaker(payload);
        else if (tab === 'feedback') await api.createFeedback(payload);
      }
      setModalOpen(false); setForm({}); fetchData(); fetchCounts();
      alert('Save successful!');
    } catch (err) { alert('Save failed: ' + err.message); }
    setSaving(false);
  };

  // ── Special actions ──
  const handleCheckin = async (regId) => {
    try { await api.checkInRegistration(regId); fetchData(); alert('Check-in successful!'); } catch (e) { alert(e.message); }
  };
  const handleCancelReg = async (regId) => {
    if (!window.confirm('Cancel this registration?')) return;
    try { await api.cancelRegistration(regId); fetchData(); alert('Registration cancelled successfully!'); } catch (e) { alert(e.message); }
  };
  const handleStartSession = async (id) => {
    try { await api.startSession(id); fetchData(); alert('Session started successfully!'); } catch (e) { alert(e.message); }
  };
  const handleEndSession = async (id) => {
    try { await api.endSession(id); fetchData(); alert('Session ended successfully!'); } catch (e) { alert(e.message); }
  };

  const handleSearch = async () => {
    if (!searchId) return;
    setLoading(true); setError('');
    try {
      let res;
      if (tab === 'events') res = await api.getEvent(searchId);
      else if (tab === 'registrations') res = await api.getRegistration(searchId);
      else if (tab === 'sessions') res = await api.getSession(searchId);
      else if (tab === 'speakers') res = await api.getSpeaker(searchId);
      else if (tab === 'feedback') res = await api.getFeedback(searchId);
      setData(res ? [res] : []);
    } catch (err) { setError(err.message); setData([]); }
    setLoading(false);
  };

  // ── Checkin Tab logic ──
  const [checkinForm, setCheckinForm] = useState({ type: 'registration', registration_code: '', registration_id: '', session_id: '', session_code: '' });
  const [checkinResult, setCheckinResult] = useState(null);
  const handleCheckinSubmit = async (e) => {
    e.preventDefault(); setCheckinResult(null);
    try {
      let res;
      if (checkinForm.type === 'registration') res = await api.checkinRegistration(checkinForm.registration_code);
      else if (checkinForm.type === 'session') res = await api.checkinSession(parseInt(checkinForm.registration_id), parseInt(checkinForm.session_id));
      else res = await api.checkinSessionCode(checkinForm.session_code, checkinForm.registration_code);
      setCheckinResult(res);
      alert('Check-in successful!');
    } catch (err) { alert('Check-in failed: ' + err.message); }
  };

  const renderCreateForm = () => {
    const F = (label, key, type = 'text', req = false, ph = '') => (
      <FormInput key={key} label={label} type={type} required={req} placeholder={ph} value={form[key] || ''} onChange={e => setForm({ ...form, [key]: e.target.value })} />
    );
    switch (tab) {
      case 'events': return <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">{F('Title *','title','text',true,'Event title')}{F('Location','location','text',false,'City or Venue')}{F('Start Date *','start_date','datetime-local',true)}{F('End Date *','end_date','datetime-local',true)}{F('Max Attendees','max_attendees','number')}{F('Organizer','organizer')}<div className="md:col-span-2">{F('Description','description','textarea')}</div></div>;
      case 'registrations': return <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">{F('Event ID *','event_id','number',true)}{F('Attendee Name *','attendee_name','text',true)}{F('Attendee Email *','attendee_email','email',true)}{F('Phone','phone')}{F('Company','company')}{F('Designation','designation')}</div>;
      case 'sessions': return <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">{F('Event ID *','event_id','number',true)}{F('Title *','title','text',true)}{F('Speaker ID','speaker_id','number')}{F('Location','location')}{F('Start Time *','start_time','datetime-local',true)}{F('End Time *','end_time','datetime-local',true)}{F('Capacity','capacity','number')}<div className="md:col-span-2">{F('Description','description','textarea')}</div></div>;
      case 'speakers': return <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">{F('Name *','name','text',true)}{F('Email *','email','email',true)}{F('Company','company')}{F('Expertise','expertise')}<div className="md:col-span-2">{F('Profile URL','profile_url')}</div><div className="md:col-span-2">{F('Bio','bio','textarea')}</div></div>;
      case 'feedback': return <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">{F('Event ID','event_id','number')}{F('Session ID','session_id','number')}{F('Registration ID','registration_id','number')}{F('Rating (1-5) *','rating','number',true)}<div className="md:col-span-2">{F('Comment','comment','textarea')}</div></div>;
      default: return null;
    }
  };

  const getColumns = () => {
    switch (tab) {
      case 'events': return ['id','title','location','start_date','end_date','max_attendees','current_attendees','status','is_active'];
      case 'registrations': return ['id','event_id','attendee_name','attendee_email','registration_code','status','is_checked_in'];
      case 'sessions': return ['id','event_id','title','speaker_id','start_time','end_time','session_code','status','current_attendees'];
      case 'speakers': return ['id','name','email','company','expertise'];
      case 'feedback': return ['_id','event_id','session_id','registration_id','rating','comment','created_at'];
      default: return [];
    }
  };

  const formatCell = (key, val) => {
    if (val === null || val === undefined) return <span className="text-slate-300 dark:text-slate-600">—</span>;
    if (key === 'is_active' || key === 'is_checked_in') return val ? <span className="text-emerald-500 bg-emerald-50 dark:bg-emerald-500/10 px-2 py-1 rounded-md text-xs font-bold">YES</span> : <span className="text-slate-400 bg-slate-50 dark:bg-slate-800 px-2 py-1 rounded-md text-xs font-bold">NO</span>;
    if (key === 'status') return <Badge text={val} color={statusColor(val)} />;
    if (key === 'rating') return <span className="text-amber-500 dark:text-amber-400 font-black">{'★'.repeat(val)}<span className="text-slate-200 dark:text-slate-700">{'★'.repeat(5 - val)}</span></span>;
    if (typeof val === 'string' && (key.includes('date') || key.includes('time') || key.includes('_at'))) {
      try { return new Date(val).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' }); } catch { return val; }
    }
    if (typeof val === 'object') return JSON.stringify(val);
    return String(val).length > 30 ? String(val).slice(0, 30) + '…' : String(val);
  };

  const cols = getColumns();
  const userRole = (user?.role || '').toUpperCase();
  const isAdmin = userRole === 'ADMIN';
  const isOrganizer = userRole === 'ORGANIZER';
  const isAdminOrOrg = isAdmin || isOrganizer;

  // RBAC: What each role can do per tab
  const canCreate = isAdminOrOrg
    ? ['events','registrations','sessions','speakers','feedback'].includes(tab)
    : ['registrations', 'feedback'].includes(tab);          // Attendee
  const canDelete = isAdmin
    ? ['events','sessions','speakers','feedback','registrations'].includes(tab)
    : isOrganizer
      ? ['events','sessions','speakers','registrations'].includes(tab)
      : ['registrations'].includes(tab);                    // Attendee can cancel own
  const canEdit = isAdminOrOrg
    ? ['events','sessions','speakers','feedback'].includes(tab)
    : false;                                                // Attendee cannot edit

  return (
    <div className="flex flex-1 overflow-hidden">
      {/* ── Sidebar ── */}
      <div className="w-64 bg-white dark:bg-dark-card border-r border-slate-200 dark:border-dark-border flex flex-col flex-shrink-0 transition-colors duration-300 relative z-10">
        <div className="p-6">
          <p className="text-xs font-bold tracking-wider text-slate-400 dark:text-slate-500 uppercase mb-3">Menu</p>
          <nav className="space-y-1">
            {tabs.map(t => (
              <button key={t.id} onClick={() => { setTab(t.id); setSearchId(''); }}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all group ${
                  tab === t.id 
                    ? 'bg-brand-50 dark:bg-brand-500/10 text-brand-600 dark:text-brand-400' 
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-dark-bg hover:text-slate-900 dark:hover:text-white'
                }`}>
                <t.icon className={`w-5 h-5 flex-shrink-0 transition-transform group-hover:scale-110 ${tab === t.id ? 'text-brand-600 dark:text-brand-400' : 'text-slate-400 dark:text-slate-500'}`} />
                {t.label}
                {counts[t.id] !== undefined && (
                  <span className={`ml-auto text-xs px-2.5 py-0.5 rounded-full font-bold ${
                    tab === t.id 
                      ? 'bg-brand-100 dark:bg-brand-500/20 text-brand-700 dark:text-brand-300' 
                      : 'bg-slate-100 dark:bg-dark-border text-slate-500 dark:text-slate-400'
                  }`}>{counts[t.id]}</span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* ── Main Area ── */}
      <div className="flex-1 flex flex-col overflow-hidden relative">
        {/* Decorative Gradients */}
        <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-brand-50 dark:from-brand-900/10 to-transparent pointer-events-none z-0"></div>
        
        {/* Header */}
        <div className="px-8 py-6 flex items-center justify-between flex-shrink-0 z-10">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white capitalize">{tab}</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Manage and organize your {tab} data.</p>
          </div>
          <div className="flex items-center gap-3">
            {tab !== 'checkins' && (
              <div className="flex items-center gap-2">
                <div className="relative group">
                  <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 group-focus-within:text-brand-500 transition-colors" />
                  <input type="text" placeholder="Search ID..." value={searchId}
                    onChange={e => setSearchId(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && handleSearch()}
                    className="pl-10 pr-4 py-2.5 bg-white dark:bg-dark-card border border-slate-200 dark:border-dark-border rounded-xl text-sm outline-none focus:ring-2 focus:ring-brand-500 dark:text-white w-48 shadow-sm transition-all" />
                </div>
                <button onClick={handleSearch} className="p-2.5 bg-white dark:bg-dark-card text-slate-500 hover:text-brand-600 dark:text-slate-400 border border-slate-200 dark:border-dark-border rounded-xl hover:border-brand-300 transition-all shadow-sm"><Search className="w-4 h-4" /></button>
              </div>
            )}
            <button onClick={() => { setSearchId(''); fetchData(); }} className="p-2.5 bg-white dark:bg-dark-card text-slate-500 hover:text-brand-600 dark:text-slate-400 border border-slate-200 dark:border-dark-border rounded-xl hover:border-brand-300 transition-all shadow-sm group" title="Refresh">
              <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
            </button>
            {canCreate && (
              <button onClick={openCreateModal}
                className="bg-brand-600 hover:bg-brand-500 text-white px-5 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 shadow-lg shadow-brand-500/30 hover:shadow-brand-500/50 transition-all hover:-translate-y-0.5">
                <Plus className="w-4 h-4" /> Add New
              </button>
            )}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto px-8 pb-8 z-10">
          {error && <div className="bg-red-50 dark:bg-red-500/10 text-red-600 dark:text-red-400 p-4 rounded-xl border border-red-200 dark:border-red-500/20 mb-6 text-sm font-semibold shadow-sm animate-fade-in">{error}</div>}

          {/* ── Checkins Tab ── */}
          {tab === 'checkins' ? (
            <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in">
              <div className="bg-white dark:bg-dark-card rounded-2xl border border-slate-200 dark:border-dark-border p-6 shadow-sm">
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-5 flex items-center gap-2"><UserCheck className="w-5 h-5 text-brand-500"/> Scan Ticket</h3>
                <div className="flex gap-2 mb-6 bg-slate-100 dark:bg-dark-bg p-1 rounded-xl">
                  {['registration','session','session-code'].map(t => (
                    <button key={t} onClick={() => setCheckinForm({ ...checkinForm, type: t })}
                      className={`flex-1 py-2 rounded-lg text-xs font-bold uppercase tracking-wide transition-all ${checkinForm.type === t ? 'bg-white dark:bg-dark-card text-brand-600 dark:text-brand-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}>
                      {t.split('-')[0]}
                    </button>
                  ))}
                </div>
                <form onSubmit={handleCheckinSubmit} className="space-y-4">
                  {checkinForm.type === 'registration' && <FormInput label="Registration Code" value={checkinForm.registration_code} onChange={e => setCheckinForm({ ...checkinForm, registration_code: e.target.value })} required />}
                  {checkinForm.type === 'session' && <><FormInput label="Registration ID" type="number" value={checkinForm.registration_id} onChange={e => setCheckinForm({ ...checkinForm, registration_id: e.target.value })} required /><FormInput label="Session ID" type="number" value={checkinForm.session_id} onChange={e => setCheckinForm({ ...checkinForm, session_id: e.target.value })} required /></>}
                  {checkinForm.type === 'session-code' && <><FormInput label="Session Code" value={checkinForm.session_code} onChange={e => setCheckinForm({ ...checkinForm, session_code: e.target.value })} required /><FormInput label="Registration Code" value={checkinForm.registration_code} onChange={e => setCheckinForm({ ...checkinForm, registration_code: e.target.value })} required /></>}
                  <button type="submit" className="w-full bg-brand-600 hover:bg-brand-500 text-white py-3 rounded-xl font-bold transition-all shadow-md shadow-brand-500/20">Verify & Check In</button>
                </form>
                {checkinResult && <div className="mt-6 bg-emerald-50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 p-4 rounded-xl border border-emerald-200 dark:border-emerald-500/20 text-sm font-mono overflow-x-auto shadow-inner animate-fade-in"><pre>{JSON.stringify(checkinResult, null, 2)}</pre></div>}
              </div>
              <div className="bg-white dark:bg-dark-card rounded-2xl border border-slate-200 dark:border-dark-border p-6 shadow-sm">
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-5 flex items-center gap-2"><ClipboardCheck className="w-5 h-5 text-brand-500"/> Check-in Stats</h3>
                <div className="space-y-6">
                  <div className="bg-slate-50 dark:bg-dark-bg p-5 rounded-xl border border-slate-100 dark:border-dark-border">
                    <FormInput label="Event ID" type="number" value={checkinForm.eventStatId || ''} onChange={e => setCheckinForm({ ...checkinForm, eventStatId: e.target.value })} />
                    <button onClick={async () => { try { const r = await api.getCheckinEventStats(checkinForm.eventStatId); setCheckinResult(r); } catch (e) { alert(e.message); } }} className="w-full bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 dark:hover:bg-slate-600 text-white py-2.5 rounded-lg text-sm font-bold transition-colors">Generate Event Report</button>
                  </div>
                  <div className="bg-slate-50 dark:bg-dark-bg p-5 rounded-xl border border-slate-100 dark:border-dark-border">
                    <FormInput label="Session ID" type="number" value={checkinForm.sessionStatId || ''} onChange={e => setCheckinForm({ ...checkinForm, sessionStatId: e.target.value })} />
                    <button onClick={async () => { try { const r = await api.getCheckinSessionStats(checkinForm.sessionStatId); setCheckinResult(r); } catch (e) { alert(e.message); } }} className="w-full bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 dark:hover:bg-slate-600 text-white py-2.5 rounded-lg text-sm font-bold transition-colors">Generate Session Report</button>
                  </div>
                </div>
              </div>
            </div>
          ) : loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="w-12 h-12 border-4 border-brand-200 dark:border-brand-900 border-t-brand-600 dark:border-t-brand-500 rounded-full animate-spin"></div>
            </div>
          ) : data.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-32 bg-white dark:bg-dark-card rounded-3xl border border-dashed border-slate-300 dark:border-dark-border shadow-sm">
              <div className="w-20 h-20 bg-slate-50 dark:bg-dark-bg rounded-full flex items-center justify-center mb-4">
                <Search className="w-8 h-8 text-slate-300 dark:text-slate-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-700 dark:text-slate-300">No {tab} found</h3>
              <p className="text-slate-400 dark:text-slate-500 mt-2 text-sm">Create a new record or adjust your search.</p>
              {canCreate && (
                <button onClick={openCreateModal} className="mt-6 bg-white dark:bg-dark-bg border border-slate-200 dark:border-dark-border text-slate-700 dark:text-white px-5 py-2.5 rounded-xl font-semibold hover:border-brand-300 transition-colors shadow-sm">
                  Create First Record
                </button>
              )}
            </div>
          ) : (
            /* ── Data Table ── */
            <div className="bg-white dark:bg-dark-card rounded-2xl border border-slate-200 dark:border-dark-border shadow-sm overflow-hidden animate-fade-in">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-50 dark:bg-dark-bg border-b border-slate-200 dark:border-dark-border">
                      {cols.map(c => (
                        <th key={c} className="px-5 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap">{c.replace(/_/g, ' ')}</th>
                      ))}
                      <th className="px-5 py-4 text-right text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-dark-border">
                    {data.map((item, idx) => (
                      <tr key={item.id || item._id || idx} className="hover:bg-slate-50/80 dark:hover:bg-white/[0.02] transition-colors group">
                        {cols.map(c => (
                          <td key={c} className="px-5 py-4 text-sm text-slate-700 dark:text-slate-300 whitespace-nowrap">{formatCell(c, item[c])}</td>
                        ))}
                        <td className="px-5 py-4 whitespace-nowrap text-right">
                          <div className="flex items-center justify-end gap-2 opacity-80 group-hover:opacity-100 transition-opacity">
                            
                            {/* Checkin action */}
                            {tab === 'registrations' && !item.is_checked_in && item.status !== 'cancelled' && (
                              <button onClick={() => handleCheckin(item.id)} className="text-emerald-600 bg-emerald-50 hover:bg-emerald-100 dark:text-emerald-400 dark:bg-emerald-500/10 dark:hover:bg-emerald-500/20 p-2 rounded-lg transition-colors border border-emerald-100 dark:border-emerald-500/20" title="Check In"><Check className="w-4 h-4" /></button>
                            )}
                            
                            {/* Cancel action */}
                            {tab === 'registrations' && item.status !== 'cancelled' && (
                              <button onClick={() => handleCancelReg(item.id)} className="text-red-500 bg-red-50 hover:bg-red-100 dark:text-red-400 dark:bg-red-500/10 dark:hover:bg-red-500/20 p-2 rounded-lg transition-colors border border-red-100 dark:border-red-500/20" title="Cancel"><X className="w-4 h-4" /></button>
                            )}
                            
                            {/* Session start/end */}
                            {tab === 'sessions' && item.status === 'scheduled' && (
                              <button onClick={() => handleStartSession(item.id)} className="text-blue-600 bg-blue-50 hover:bg-blue-100 dark:text-blue-400 dark:bg-blue-500/10 dark:hover:bg-blue-500/20 p-2 rounded-lg transition-colors border border-blue-100 dark:border-blue-500/20" title="Start Session"><Play className="w-4 h-4" /></button>
                            )}
                            {tab === 'sessions' && item.status === 'ongoing' && (
                              <button onClick={() => handleEndSession(item.id)} className="text-amber-600 bg-amber-50 hover:bg-amber-100 dark:text-amber-400 dark:bg-amber-500/10 dark:hover:bg-amber-500/20 p-2 rounded-lg transition-colors border border-amber-100 dark:border-amber-500/20" title="End Session"><Square className="w-4 h-4" /></button>
                            )}
                            
                            {/* Edit Action */}
                            {canEdit && tab !== 'registrations' && (
                              <button onClick={() => openEditModal(item)} className="text-slate-600 bg-slate-100 hover:bg-slate-200 dark:text-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700 p-2 rounded-lg transition-colors border border-slate-200 dark:border-slate-700" title="Edit"><Edit2 className="w-4 h-4" /></button>
                            )}

                            {/* Delete Action */}
                            {canDelete && (
                              <button onClick={() => handleDelete(item.id || item._id)} className="text-red-500 bg-red-50 hover:bg-red-100 dark:text-red-400 dark:bg-red-500/10 dark:hover:bg-red-500/20 p-2 rounded-lg transition-colors border border-red-100 dark:border-red-500/20" title="Delete"><Trash2 className="w-4 h-4" /></button>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="px-5 py-3 bg-slate-50 dark:bg-dark-bg border-t border-slate-200 dark:border-dark-border flex justify-between items-center">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Total Records: {data.length}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Create/Edit Modal ── */}
      {modalOpen && (
        <Modal title={isEditing ? `Edit ${tab.slice(0, -1)}` : `Add New ${tab.slice(0, -1)}`} onClose={() => setModalOpen(false)}>
          <form onSubmit={handleSave} className="space-y-4">
            {renderCreateForm()}
            <div className="flex justify-end gap-3 pt-6 border-t border-slate-200 dark:border-dark-border mt-6">
              <button type="button" onClick={() => setModalOpen(false)} className="px-5 py-2.5 text-sm font-bold text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-dark-bg rounded-xl hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors">Cancel</button>
              <button type="submit" disabled={saving} className="px-5 py-2.5 text-sm font-bold text-white bg-brand-600 rounded-xl hover:bg-brand-500 disabled:opacity-50 flex items-center gap-2 transition-all shadow-lg shadow-brand-500/30 hover:shadow-brand-500/50">
                {saving ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> : isEditing ? <Check className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                {isEditing ? 'Save Changes' : 'Create'}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default Dashboard;
