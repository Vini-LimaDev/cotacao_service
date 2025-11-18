// src/contexts/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8888';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Carregar token do localStorage ao iniciar
  useEffect(() => {
    const savedToken = localStorage.getItem('access_token');
    if (savedToken) {
      setToken(savedToken);
      loadUserProfile(savedToken);
    } else {
      setLoading(false);
    }
  }, []);

  // Carregar perfil do usuário
  async function loadUserProfile(authToken) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // Token inválido, limpar
        logout();
      }
    } catch (error) {
      console.error('Erro ao carregar perfil:', error);
      logout();
    } finally {
      setLoading(false);
    }
  }

  // Função de login
  async function login(email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao fazer login');
      }

      const data = await response.json();
      const accessToken = data.access_token;

      // Salvar token
      localStorage.setItem('access_token', accessToken);
      setToken(accessToken);

      // Carregar dados do usuário
      await loadUserProfile(accessToken);

      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Função de registro
  async function register(email, password, fullName) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          full_name: fullName,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao criar conta');
      }

      const userData = await response.json();
      
      // Após registrar, fazer login automaticamente
      return await login(email, password);
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Função de logout
  function logout() {
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
  }

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider');
  }
  return context;
}
