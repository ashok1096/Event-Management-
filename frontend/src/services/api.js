const API_BASE_URL = 'http://localhost:8000';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

const handleResponse = async (res) => {
  if (res.status === 204) return { success: true };
  const text = await res.text();
  if (!res.ok) {
    let msg = 'Request failed';
    try { const d = JSON.parse(text); msg = d.detail || msg; } catch {}
    throw new Error(msg);
  }
  if (!text) return { success: true };
  try { return JSON.parse(text); } catch { return { success: true }; }
};

// ── AUTH ──
export const authRegister = (name, email, password, role = 'admin') =>
  fetch(`${API_BASE_URL}/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, email, password, role }) }).then(handleResponse);

export const authLogin = (email, password) =>
  fetch(`${API_BASE_URL}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) }).then(handleResponse);

export const authMe = () =>
  fetch(`${API_BASE_URL}/auth/me`, { headers: getHeaders() }).then(handleResponse);

// ── EVENTS ──
export const getEvents = (skip = 0, limit = 100) =>
  fetch(`${API_BASE_URL}/events/?skip=${skip}&limit=${limit}`, { headers: getHeaders() }).then(handleResponse);
export const getEvent = (id) =>
  fetch(`${API_BASE_URL}/events/${id}`, { headers: getHeaders() }).then(handleResponse);
export const createEvent = (data) =>
  fetch(`${API_BASE_URL}/events/`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const updateEvent = (id, data) =>
  fetch(`${API_BASE_URL}/events/${id}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const deleteEvent = (id) =>
  fetch(`${API_BASE_URL}/events/${id}`, { method: 'DELETE', headers: getHeaders() }).then(handleResponse);
export const getEventStats = (id) =>
  fetch(`${API_BASE_URL}/events/${id}/stats`, { headers: getHeaders() }).then(handleResponse);

// ── REGISTRATIONS ──
export const createRegistration = (data) =>
  fetch(`${API_BASE_URL}/registrations/`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const getRegistration = (id) =>
  fetch(`${API_BASE_URL}/registrations/${id}`, { headers: getHeaders() }).then(handleResponse);
export const getRegistrationsByEvent = (eventId, skip = 0, limit = 100) =>
  fetch(`${API_BASE_URL}/registrations/event/${eventId}?skip=${skip}&limit=${limit}`, { headers: getHeaders() }).then(handleResponse);
export const getRegistrationsByEmail = (email) =>
  fetch(`${API_BASE_URL}/registrations/email/${email}`, { headers: getHeaders() }).then(handleResponse);
export const updateRegistration = (id, data) =>
  fetch(`${API_BASE_URL}/registrations/${id}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const checkInRegistration = (id) =>
  fetch(`${API_BASE_URL}/registrations/${id}/check-in`, { method: 'POST', headers: getHeaders() }).then(handleResponse);
export const cancelRegistration = (id) =>
  fetch(`${API_BASE_URL}/registrations/${id}/cancel`, { method: 'DELETE', headers: getHeaders() }).then(handleResponse);
export const getRegistrationStats = (eventId) =>
  fetch(`${API_BASE_URL}/registrations/event/${eventId}/stats`, { headers: getHeaders() }).then(handleResponse);

// ── SESSIONS ──
export const getSessions = (skip = 0, limit = 100) =>
  fetch(`${API_BASE_URL}/sessions/?skip=${skip}&limit=${limit}`, { headers: getHeaders() }).then(handleResponse);
export const getSession = (id) =>
  fetch(`${API_BASE_URL}/sessions/${id}`, { headers: getHeaders() }).then(handleResponse);
export const createSession = (data) =>
  fetch(`${API_BASE_URL}/sessions/`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const updateSession = (id, data) =>
  fetch(`${API_BASE_URL}/sessions/${id}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const deleteSession = (id) =>
  fetch(`${API_BASE_URL}/sessions/${id}`, { method: 'DELETE', headers: getHeaders() }).then(handleResponse);
export const startSession = (id) =>
  fetch(`${API_BASE_URL}/sessions/${id}/start`, { method: 'POST', headers: getHeaders() }).then(handleResponse);
export const endSession = (id) =>
  fetch(`${API_BASE_URL}/sessions/${id}/end`, { method: 'POST', headers: getHeaders() }).then(handleResponse);
export const getSessionAttendance = (id) =>
  fetch(`${API_BASE_URL}/sessions/${id}/attendance`, { headers: getHeaders() }).then(handleResponse);

// ── CHECKINS ──
export const checkinRegistration = (registration_code) =>
  fetch(`${API_BASE_URL}/checkins/registration-checkin`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(registration_code) }).then(handleResponse);
export const checkinSession = (registration_id, session_id) =>
  fetch(`${API_BASE_URL}/checkins/session-checkin`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ registration_id, session_id }) }).then(handleResponse);
export const checkinSessionCode = (session_code, registration_code) =>
  fetch(`${API_BASE_URL}/checkins/session-code-checkin`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ session_code, registration_code }) }).then(handleResponse);
export const getCheckinEventStats = (eventId) =>
  fetch(`${API_BASE_URL}/checkins/event/${eventId}/stats`, { headers: getHeaders() }).then(handleResponse);
export const getCheckinSessionStats = (sessionId) =>
  fetch(`${API_BASE_URL}/checkins/session/${sessionId}/stats`, { headers: getHeaders() }).then(handleResponse);

// ── SPEAKERS ──
export const getSpeakers = (skip = 0, limit = 100) =>
  fetch(`${API_BASE_URL}/speakers/?skip=${skip}&limit=${limit}`, { headers: getHeaders() }).then(handleResponse);
export const getSpeaker = (id) =>
  fetch(`${API_BASE_URL}/speakers/${id}`, { headers: getHeaders() }).then(handleResponse);
export const createSpeaker = (data) =>
  fetch(`${API_BASE_URL}/speakers/`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const updateSpeaker = (id, data) =>
  fetch(`${API_BASE_URL}/speakers/${id}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const deleteSpeaker = (id) =>
  fetch(`${API_BASE_URL}/speakers/${id}`, { method: 'DELETE', headers: getHeaders() }).then(handleResponse);
export const getSpeakerSessions = (id) =>
  fetch(`${API_BASE_URL}/speakers/${id}/sessions`, { headers: getHeaders() }).then(handleResponse);

// ── FEEDBACK (MongoDB) ──
export const getFeedbacks = () =>
  fetch(`${API_BASE_URL}/feedback/`, { headers: getHeaders() }).then(handleResponse);
export const getFeedback = (id) =>
  fetch(`${API_BASE_URL}/feedback/${id}`, { headers: getHeaders() }).then(handleResponse);
export const createFeedback = (data) =>
  fetch(`${API_BASE_URL}/feedback/`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const updateFeedback = (id, data) =>
  fetch(`${API_BASE_URL}/feedback/${id}`, { method: 'PUT', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse);
export const deleteFeedback = (id) =>
  fetch(`${API_BASE_URL}/feedback/${id}`, { method: 'DELETE', headers: getHeaders() }).then(handleResponse);
