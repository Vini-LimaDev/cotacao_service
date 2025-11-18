// src/components/CriptoPage.jsx
import { useState, useEffect, useRef } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8888';
const REFRESH_INTERVAL_MS = 30000; // Atualiza a cada 30 segundos (evita rate limit)

export default function CriptoPage() {
  const [cotacoes, setCotacoes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);
  
  // Valores para conversão USDT
  const [valorUSDT, setValorUSDT] = useState('');
  const [valorBRLfromUSDT, setValorBRLfromUSDT] = useState('');
  
  // Valores para conversão USDC
  const [valorUSDC, setValorUSDC] = useState('');
  const [valorBRLfromUSDC, setValorBRLfromUSDC] = useState('');
  
  const [mostrarNotificacao, setMostrarNotificacao] = useState(false);
  const [proximaAtualizacao, setProximaAtualizacao] = useState(REFRESH_INTERVAL_MS / 1000);
  const intervalRef = useRef(null);
  const countdownRef = useRef(null);

  // Busca cotações automaticamente ao montar o componente
  useEffect(() => {
    buscarCotacoesAutomatica();
    
    // Configura o auto-refresh
    intervalRef.current = setInterval(() => {
      buscarCotacoesAutomatica();
    }, REFRESH_INTERVAL_MS);

    // Cleanup ao desmontar
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
      }
    };
  }, []);

  // Efeito para esconder a notificação após 4 segundos
  useEffect(() => {
    if (mostrarNotificacao) {
      const timer = setTimeout(() => {
        setMostrarNotificacao(false);
      }, 4000);
      
      return () => clearTimeout(timer);
    }
  }, [mostrarNotificacao]);

  // Countdown para próxima atualização
  useEffect(() => {
    // Inicia o countdown
    setProximaAtualizacao(REFRESH_INTERVAL_MS / 1000);
    
    countdownRef.current = setInterval(() => {
      setProximaAtualizacao(prev => {
        if (prev <= 1) {
          return REFRESH_INTERVAL_MS / 1000;
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
      }
    };
  }, [cotacoes]); // Reinicia quando cotações mudam

  // Função para buscar cotações automaticamente
  async function buscarCotacoesAutomatica() {
    setLoading(true);
    setErro(null);

    try {
      const resp = await fetch(`${API_BASE_URL}/cripto/ambas-brl`);
      if (!resp.ok) {
        const body = await resp.json().catch(() => ({}));
        
        // Mensagem específica para rate limit
        if (resp.status === 502 && body.detail?.includes('429')) {
          throw new Error('Limite de requisições atingido. Aguarde 30 segundos...');
        }
        
        throw new Error(body.detail || 'Erro ao buscar cotações');
      }

      const data = await resp.json();
      setCotacoes(data);
      
      // Mostra notificação de sucesso
      setMostrarNotificacao(true);
      
      // Recalcula conversões se houver valores
      if (valorUSDT && !isNaN(parseFloat(valorUSDT)) && data.USDT) {
        calcularConversaoUSDT(parseFloat(valorUSDT), data.USDT.taxa_cambio);
      }
      if (valorUSDC && !isNaN(parseFloat(valorUSDC)) && data.USDC) {
        calcularConversaoUSDC(parseFloat(valorUSDC), data.USDC.taxa_cambio);
      }
    } catch (err) {
      console.error(err);
      setErro(err.message || 'Erro inesperado');
      // Não limpa as cotações em caso de erro - mantém os últimos valores
    } finally {
      setLoading(false);
    }
  }

  // Função para buscar cotações manualmente
  async function buscarCotacoes(e) {
    e.preventDefault();
    buscarCotacoesAutomatica();
  }

  // Funções para calcular conversão USDT
  function calcularConversaoUSDT(valor, taxa) {
    if (!taxa) return;
    const resultado = valor * taxa;
    setValorBRLfromUSDT(resultado.toFixed(2));
  }

  function handleValorUSDTChange(e) {
    const valor = e.target.value;
    setValorUSDT(valor);
    
    if (cotacoes?.USDT && valor && !isNaN(parseFloat(valor))) {
      calcularConversaoUSDT(parseFloat(valor), cotacoes.USDT.taxa_cambio);
    } else {
      setValorBRLfromUSDT('');
    }
  }

  function handleValorBRLfromUSDTChange(e) {
    const valor = e.target.value;
    setValorBRLfromUSDT(valor);
    
    if (cotacoes?.USDT && valor && !isNaN(parseFloat(valor)) && cotacoes.USDT.taxa_cambio !== 0) {
      const resultado = parseFloat(valor) / cotacoes.USDT.taxa_cambio;
      setValorUSDT(resultado.toFixed(2));
    } else {
      setValorUSDT('');
    }
  }

  // Funções para calcular conversão USDC
  function calcularConversaoUSDC(valor, taxa) {
    if (!taxa) return;
    const resultado = valor * taxa;
    setValorBRLfromUSDC(resultado.toFixed(2));
  }

  function handleValorUSDCChange(e) {
    const valor = e.target.value;
    setValorUSDC(valor);
    
    if (cotacoes?.USDC && valor && !isNaN(parseFloat(valor))) {
      calcularConversaoUSDC(parseFloat(valor), cotacoes.USDC.taxa_cambio);
    } else {
      setValorBRLfromUSDC('');
    }
  }

  function handleValorBRLfromUSDCChange(e) {
    const valor = e.target.value;
    setValorBRLfromUSDC(valor);
    
    if (cotacoes?.USDC && valor && !isNaN(parseFloat(valor)) && cotacoes.USDC.taxa_cambio !== 0) {
      const resultado = parseFloat(valor) / cotacoes.USDC.taxa_cambio;
      setValorUSDC(resultado.toFixed(2));
    } else {
      setValorUSDC('');
    }
  }

  function formatarData(isoString) {
    if (!isoString) return '';
    const d = new Date(isoString);
    return d.toLocaleString('pt-BR');
  }

  return (
    <div className="cripto-container">
      <div className="cripto-header-section">
        <div>
          <h1 className="title">Cotação de Criptomoedas</h1>
          <p className="subtitle">
            {cotacoes ? `Fonte: ${cotacoes.USDT?.fonte || cotacoes.USDC?.fonte || 'API'}` : 'Consumindo API em tempo real'}
          </p>
        </div>
        <div className="auto-refresh-info">
          <div className="refresh-badge">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M13.65 2.35C12.2 0.9 10.21 0 8 0 3.58 0 0.01 3.58 0.01 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L9 7h7V0l-2.35 2.35z" fill="currentColor"/>
            </svg>
            <span>Atualiza em {proximaAtualizacao}s</span>
          </div>
        </div>
      </div>

      <form className="form" onSubmit={buscarCotacoes}>
        <div className="actions">
          <button type="submit" disabled={loading}>
            {loading ? 'Buscando...' : 'Atualizar agora'}
          </button>
        </div>
      </form>

      {erro && (
        <div className="alert alert-error">
          <strong>⚠️ Erro:</strong> {erro}
          {erro.includes('Limite') && (
            <p className="erro-hint">
              A API CoinGecko possui limite de requisições gratuitas. 
              As cotações serão atualizadas automaticamente quando o limite for resetado.
            </p>
          )}
        </div>
      )}

      {cotacoes && (
        <div className="cripto-grid">
          {/* Card USDT */}
          {cotacoes.USDT && (
            <div className="cripto-card">
              <div className="cripto-header">
                <h2>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style={{verticalAlign: 'middle', marginRight: '8px'}}>
                    <circle cx="12" cy="12" r="10" fill="#50AF95"/>
                    <path d="M13.5 10.5V9h3V7.5h-9V9h3v1.5c-2.5.3-4.5 1.3-4.5 2.5s2 2.2 4.5 2.5V18h1.5v-2.5c2.5-.3 4.5-1.3 4.5-2.5s-2-2.2-4.5-2.5zm-3 3.8c-1.7-.2-3-.8-3-1.3s1.3-1.1 3-1.3v2.6zm3 0v-2.6c1.7.2 3 .8 3 1.3s-1.3 1.1-3 1.3z" fill="white"/>
                  </svg>
                  USDT (Tether)
                </h2>
                <span className="badge badge-api">
                  {cotacoes.USDT.fonte}
                </span>
              </div>

              <div className="cripto-info">
                <div className="result-row">
                  <span>Símbolo:</span>
                  <strong>{cotacoes.USDT.simbolo}</strong>
                </div>
                <div className="result-row">
                  <span>Moeda:</span>
                  <strong>{cotacoes.USDT.moeda_destino}</strong>
                </div>
                <div className="result-row">
                  <span>Taxa de câmbio:</span>
                  <strong className="taxa-destaque">
                    R$ {cotacoes.USDT.taxa_cambio.toFixed(4)}
                  </strong>
                </div>
                <div className="result-row">
                  <span>Atualizado:</span>
                  <span className="data-atualizacao">
                    {formatarData(cotacoes.USDT.data_cotacao)}
                  </span>
                </div>
              </div>

              <div className="conversion-section">
                <h3>Converter USDT</h3>
                <div className="field-row">
                  <div className="field">
                    <label>USDT</label>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      value={valorUSDT}
                      onChange={handleValorUSDTChange}
                    />
                  </div>
                  <div className="conversion-arrow">→</div>
                  <div className="field">
                    <label>BRL</label>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      value={valorBRLfromUSDT}
                      onChange={handleValorBRLfromUSDTChange}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Card USDC */}
          {cotacoes.USDC && (
            <div className="cripto-card">
              <div className="cripto-header">
                <h2>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style={{verticalAlign: 'middle', marginRight: '8px'}}>
                    <circle cx="12" cy="12" r="10" fill="#2775CA"/>
                    <path d="M15.5 12c0-1.93-1.57-3.5-3.5-3.5S8.5 10.07 8.5 12s1.57 3.5 3.5 3.5 3.5-1.57 3.5-3.5zm-5.25 0c0-.97.78-1.75 1.75-1.75s1.75.78 1.75 1.75-.78 1.75-1.75 1.75-1.75-.78-1.75-1.75z" fill="white"/>
                    <path d="M12 6.5c-.55 0-1 .45-1 1v.75c-1.24.26-2.25 1.24-2.25 2.5h1.5c0-.69.56-1.25 1.25-1.25h1c.69 0 1.25.56 1.25 1.25 0 .55-.36 1.03-.87 1.19l-2 .63c-.95.3-1.63 1.16-1.63 2.18 0 1.26 1.01 2.24 2.25 2.5v.75c0 .55.45 1 1 1s1-.45 1-1v-.75c1.24-.26 2.25-1.24 2.25-2.5h-1.5c0 .69-.56 1.25-1.25 1.25h-1c-.69 0-1.25-.56-1.25-1.25 0-.55.36-1.03.87-1.19l2-.63c.95-.3 1.63-1.16 1.63-2.18 0-1.26-1.01-2.24-2.25-2.5V7.5c0-.55-.45-1-1-1z" fill="white"/>
                  </svg>
                  USDC (USD Coin)
                </h2>
                <span className="badge badge-api">
                  {cotacoes.USDC.fonte}
                </span>
              </div>

              <div className="cripto-info">
                <div className="result-row">
                  <span>Símbolo:</span>
                  <strong>{cotacoes.USDC.simbolo}</strong>
                </div>
                <div className="result-row">
                  <span>Moeda:</span>
                  <strong>{cotacoes.USDC.moeda_destino}</strong>
                </div>
                <div className="result-row">
                  <span>Taxa de câmbio:</span>
                  <strong className="taxa-destaque">
                    R$ {cotacoes.USDC.taxa_cambio.toFixed(4)}
                  </strong>
                </div>
                <div className="result-row">
                  <span>Atualizado:</span>
                  <span className="data-atualizacao">
                    {formatarData(cotacoes.USDC.data_cotacao)}
                  </span>
                </div>
              </div>

              <div className="conversion-section">
                <h3>Converter USDC</h3>
                <div className="field-row">
                  <div className="field">
                    <label>USDC</label>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      value={valorUSDC}
                      onChange={handleValorUSDCChange}
                    />
                  </div>
                  <div className="conversion-arrow">→</div>
                  <div className="field">
                    <label>BRL</label>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      value={valorBRLfromUSDC}
                      onChange={handleValorBRLfromUSDCChange}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

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
          <span>Cotações atualizadas com sucesso!</span>
        </div>
      )}
    </div>
  );
}
