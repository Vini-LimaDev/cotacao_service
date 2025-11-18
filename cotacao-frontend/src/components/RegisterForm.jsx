// src/components/RegisterForm.jsx
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function RegisterForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');

    // Validações
    if (password !== confirmPassword) {
      setError('As senhas não coincidem');
      return;
    }

    if (password.length < 6) {
      setError('A senha deve ter no mínimo 6 caracteres');
      return;
    }

    setLoading(true);

    const result = await register(email, password, fullName);

    if (!result.success) {
      setError(result.error);
      setLoading(false);
    }
    // Se sucesso, o AuthContext vai fazer login automaticamente
  }

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <h2>Criar Conta</h2>
      <p className="auth-subtitle">
        Registre-se para acessar o sistema de cotações
      </p>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="field">
        <label htmlFor="register-name">Nome Completo</label>
        <input
          id="register-name"
          type="text"
          placeholder="Seu nome"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          autoComplete="name"
        />
      </div>

      <div className="field">
        <label htmlFor="register-email">Email</label>
        <input
          id="register-email"
          type="email"
          placeholder="seu@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
      </div>

      <div className="field">
        <label htmlFor="register-password">Senha</label>
        <input
          id="register-password"
          type="password"
          placeholder="Mínimo 6 caracteres"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
          autoComplete="new-password"
        />
      </div>

      <div className="field">
        <label htmlFor="register-confirm">Confirmar Senha</label>
        <input
          id="register-confirm"
          type="password"
          placeholder="Digite a senha novamente"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          minLength={6}
          autoComplete="new-password"
        />
      </div>

      <button
        type="submit"
        className="btn-primary"
        disabled={loading}
      >
        {loading ? 'Criando conta...' : 'Criar Conta'}
      </button>
    </form>
  );
}
