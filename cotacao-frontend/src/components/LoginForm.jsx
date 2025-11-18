// src/components/LoginForm.jsx
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);

    if (!result.success) {
      setError(result.error);
      setLoading(false);
    }
    // Se sucesso, o AuthContext vai redirecionar automaticamente
  }

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <h2>Entrar</h2>
      <p className="auth-subtitle">
        Acesse sua conta para consultar cotações
      </p>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="field">
        <label htmlFor="login-email">Email</label>
        <input
          id="login-email"
          type="email"
          placeholder="seu@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
      </div>

      <div className="field">
        <label htmlFor="login-password">Senha</label>
        <input
          id="login-password"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
          autoComplete="current-password"
        />
      </div>

      <button
        type="submit"
        className="btn-primary"
        disabled={loading}
      >
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  );
}
