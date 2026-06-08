import { BrowserRouter, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import { LogOut, User as UserIcon, Zap, Moon, Sun, Info, LayoutDashboard } from 'lucide-react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider, useTheme } from './contexts/ThemeContext';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import About from './pages/About';
import EventListing from './pages/EventListing';
import EventDetail from './pages/EventDetail';
import Registration from './pages/Registration';
import ChatWidget from './components/ChatWidget';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { isDark, toggleTheme } = useTheme();
  const location = useLocation();
  
  if (!user) return null;
  return (
    <nav className="h-16 bg-white/80 dark:bg-dark-card/80 backdrop-blur-md border-b border-slate-200 dark:border-dark-border px-6 flex items-center justify-between flex-shrink-0 z-50 sticky top-0 transition-colors duration-300">
      <Link to="/" className="flex items-center gap-3 group">
        <div className="bg-brand-600 dark:bg-brand-500 p-1.5 rounded-xl shadow-glow dark:shadow-glow-dark group-hover:scale-105 transition-transform">
          <Zap className="h-5 w-5 text-white" />
        </div>
        <span className="text-xl font-bold text-slate-800 dark:text-slate-100 tracking-tight">EventPulse</span>
      </Link>
      
      <div className="flex items-center gap-2 md:gap-6">
        
        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-1 bg-slate-100 dark:bg-dark-bg p-1 rounded-xl border border-slate-200 dark:border-dark-border">
          <Link to="/" className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-bold transition-all ${location.pathname === '/' ? 'bg-white dark:bg-dark-card text-brand-600 dark:text-brand-400 shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'}`}>
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </Link>
          <Link to="/about" className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-bold transition-all ${location.pathname === '/about' ? 'bg-white dark:bg-dark-card text-brand-600 dark:text-brand-400 shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white'}`}>
            <Info className="w-4 h-4" /> About
          </Link>
        </div>

        <div className="h-6 w-px bg-slate-200 dark:bg-dark-border hidden md:block"></div>
        
        <button 
          onClick={toggleTheme}
          className="p-2 text-slate-500 hover:text-brand-600 dark:text-slate-400 dark:hover:text-brand-400 bg-slate-100 hover:bg-slate-200 dark:bg-dark-bg dark:hover:bg-slate-800 rounded-full transition-all"
          title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
        
        <div className="h-6 w-px bg-slate-200 dark:bg-dark-border"></div>
        
        <div className="flex items-center gap-3">
          <span className="text-sm font-bold text-slate-700 dark:text-slate-200 flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-brand-100 dark:bg-brand-900/50 flex items-center justify-center border border-brand-200 dark:border-brand-800">
              <UserIcon className="w-4 h-4 text-brand-600 dark:text-brand-400" />
            </div>
            <span className="hidden sm:inline">{user.name || user.email}</span>
          </span>
          
          <button 
            onClick={logout} 
            className="text-sm text-red-600 hover:text-white font-bold flex items-center gap-1.5 bg-red-50 hover:bg-red-500 dark:bg-red-500/10 dark:hover:bg-red-500 dark:text-red-400 border border-red-100 dark:border-red-500/20 px-3 py-1.5 rounded-lg transition-all shadow-sm group"
          >
            <LogOut className="h-4 w-4 group-hover:-translate-x-1 transition-transform" /> 
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </nav>
  );
};

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/login" />;
  return children;
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <div className="h-screen flex flex-col bg-slate-50 dark:bg-dark-bg text-slate-900 dark:text-dark-text overflow-hidden transition-colors duration-500">
            <Navbar />
            <Routes>
              <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
              <Route path="/about" element={<ProtectedRoute><About /></ProtectedRoute>} />
              <Route path="/events" element={<ProtectedRoute><EventListing /></ProtectedRoute>} />
              <Route path="/events/:id" element={<ProtectedRoute><EventDetail /></ProtectedRoute>} />
              <Route path="/events/:id/register" element={<ProtectedRoute><Registration /></ProtectedRoute>} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Routes>
            <ChatWidget />
          </div>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
