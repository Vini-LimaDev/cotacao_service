import { useState, useEffect } from 'react';

const MOEDAS = ['USD', 'EUR', 'BRL', 'JPY'];

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:9876';

function App() {
  const [moedaOrigem, setMoedaOrigem] = useState('USD');
  const [moedaDestino, setMoedaDestino] = useState('BRL');
  const [cotacao, setCotacao] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);
  const [valorOrigem, setValorOrigem] = useState('');
  const [valorDestino, setValorDestino] = useState('');
  const [mostrarNotificacao, setMostrarNotificacao] = useState(false);

  // Busca cotação automaticamente quando as moedas mudarem
  useEffect(() => {
    if (moedaOrigem !== moedaDestino) {
      buscarCotacaoAutomatica();
    }
  }, [moedaOrigem, moedaDestino]);

  // Efeito para esconder a notificação após 4 segundos
  useEffect(() => {
    if (mostrarNotificacao) {
      const timer = setTimeout(() => {
        setMostrarNotificacao(false);
      }, 4000);
      
      return () => clearTimeout(timer);
    }
  }, [mostrarNotificacao]);

  async function buscarCotacaoAutomatica() {
    setLoading(true);
    setErro(null);

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
      
      // Mostra notificação de sucesso
      setMostrarNotificacao(true);
      
      // Recalcula a conversão se houver valor
      if (valorOrigem && !isNaN(parseFloat(valorOrigem))) {
        calcularConversao(parseFloat(valorOrigem), data.taxa_cambio);
      } else if (valorDestino && !isNaN(parseFloat(valorDestino))) {
        // Recalcula também se houver valor no campo de destino
        const resultado = parseFloat(valorDestino) / data.taxa_cambio;
        setValorOrigem(resultado.toFixed(2));
      }
    } catch (err) {
      console.error(err);
      setErro(err.message || 'Erro inesperado');
      setCotacao(null);
    } finally {
      setLoading(false);
    }
  }

  async function buscarCotacao(e) {
    e.preventDefault();
    buscarCotacaoAutomatica();
  }

  function calcularConversao(valor, taxa) {
    if (!taxa) return;
    const resultado = valor * taxa;
    setValorDestino(resultado.toFixed(2));
  }

  function handleValorOrigemChange(e) {
    const valor = e.target.value;
    setValorOrigem(valor);
    
    if (cotacao && valor && !isNaN(parseFloat(valor))) {
      calcularConversao(parseFloat(valor), cotacao.taxa_cambio);
    } else {
      setValorDestino('');
    }
  }

  function handleValorDestinoChange(e) {
    const valor = e.target.value;
    setValorDestino(valor);
    
    if (cotacao && valor && !isNaN(parseFloat(valor)) && cotacao.taxa_cambio !== 0) {
      const resultado = parseFloat(valor) / cotacao.taxa_cambio;
      setValorOrigem(resultado.toFixed(2));
    } else {
      setValorOrigem('');
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

            <div className="conversion-section">
              <h3>Converter valores</h3>
              <div className="field-row">
                <div className="field">
                  <label>{cotacao.moeda_origem}</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    placeholder="0.00"
                    value={valorOrigem}
                    onChange={handleValorOrigemChange}
                  />
                </div>
                <div className="conversion-arrow">→</div>
                <div className="field">
                  <label>{cotacao.moeda_destino}</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    placeholder="0.00"
                    value={valorDestino}
                    onChange={handleValorDestinoChange}
                  />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Notificação Toast */}
      {mostrarNotificacao && (
        <div className="toast-notification">
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M10 0C4.477 0 0 4.477 0 10C0 15.523 4.477 20 10 20C15.523 20 20 15.523 20 10C20 4.477 15.523 0 10 0ZM8 15L3 10L4.41 8.59L8 12.17L15.59 4.58L17 6L8 15Z"
              fill="currentColor"
            />
          </svg>
          <span>Cotação atualizada com sucesso!</span>
        </div>
      )}
    </div>
  );
}

export default App;
