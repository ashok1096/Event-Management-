import { createContext, useContext, useState, useEffect } from 'react';
import { authLogin, authMe } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await authMe();
          setUser(userData);
        } catch (error) {
          console.error('Token invalid, clearing', error);
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const handleLogin = async (email, password) => {
    const data = await authLogin(email, password);
    localStorage.setItem('token', data.access_token);
    const userData = await authMe();
    setUser(userData);
    return userData;
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login: handleLogin, logout: handleLogout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
