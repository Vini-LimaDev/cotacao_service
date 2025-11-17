import { useState } from 'react';

const MOEDAS = ['USD', 'EUR', 'BRL', 'JPY'];

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:9876';

function App() {
  const [moedaOrigem, setMoedaOrigem] = useState('USD');
  const [moedaDestino, setMoedaDestino] = useState('BRL');
  const [cotacao, setCotacao] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);

  async function buscarCotacao(e) {
    e.preventDefault();
    setLoading(true);
    setErro(null);
    setCotacao(null);

    try {
      const params = new URLSearchParams({
        moeda_origem: moedaOrigem,
        moeda_destino: moedaDestino,
      });

      const resp = await fetch(`${API_BASE_URL}/cotacao?${params.toString()}`);
      if (!resp.ok) {
        const body = await resp.json().catch(() => ({}));
        throw new Error(body.detail || 'Erro ao buscar cotação');
      }

      const data = await resp.json();
      setCotacao(data);
    } catch (err) {
      console.error(err);
      setErro(err.message || 'Erro inesperado');
    } finally {
      setLoading(false);
    }
  }

  function formatarData(isoString) {
    if (!isoString) return '';
    const d = new Date(isoString);
    return d.toLocaleString('pt-BR');
  }

  return (
    <div className="app-root">
      <div className="card">
        <h1 className="title">Cotação de Moedas</h1>
        <p className="subtitle">
          Consumindo a API em <code>/cotacao</code> com cache em memória.
        </p>

        <form className="form" onSubmit={buscarCotacao}>
          <div className="field-row">
            <div className="field">
              <label>Moeda de origem</label>
              <select
                value={moedaOrigem}
                onChange={e => setMoedaOrigem(e.target.value)}
              >
                {MOEDAS.map(m => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label>Moeda de destino</label>
              <select
                value={moedaDestino}
                onChange={e => setMoedaDestino(e.target.value)}
              >
                {MOEDAS.map(m => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="actions">
            <button
              type="submit"
              disabled={loading || moedaOrigem === moedaDestino}
            >
              {loading ? 'Buscando...' : 'Buscar cotação'}
            </button>
          </div>

          {moedaOrigem === moedaDestino && (
            <p className="hint">
              Escolha moedas diferentes para calcular a taxa de câmbio.
            </p>
          )}
        </form>

        {erro && (
          <div className="alert alert-error">
            <strong>Erro:</strong> {erro}
          </div>
        )}

        {cotacao && (
          <div className="result-card">
            <div className="result-row">
              <span>Par:</span>
              <strong>
                {cotacao.moeda_origem} → {cotacao.moeda_destino}
              </strong>
            </div>
            <div className="result-row">
              <span>Taxa de câmbio:</span>
              <strong>{cotacao.taxa_cambio}</strong>
            </div>
            <div className="result-row">
              <span>Atualizado em:</span>
              <span>{formatarData(cotacao.data_cotacao)}</span>
            </div>
            <div className="result-row">
              <span>Fonte:</span>
              <span className={`badge badge-${cotacao.fonte}`}>
                {cotacao.fonte === 'cache' ? 'Cache' : 'API Externa'}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
