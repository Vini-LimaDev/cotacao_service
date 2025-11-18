# Providers de Criptomoedas

Este documento explica como gerenciar os diferentes providers de cotações de criptomoedas.

## 🔄 Providers Disponíveis

### 1. **Binance API** (Atual - Padrão)
- ✅ **Status**: Ativo e recomendado
- 🌐 **Endpoint**: `https://api.binance.com/api/v3`
- 📊 **Rate Limit**: 1200 requisições/minuto
- 🔑 **Autenticação**: Não necessária para dados públicos
- 💰 **Custo**: Gratuito
- 🎯 **Ideal para**: Produção, alta disponibilidade

**Endpoints usados:**
- `/ticker/price?symbol=USDTBRL`
- `/ticker/price?symbol=USDCBRL`

---

### 2. **CoinGecko API** (Alternativa)
- ⚠️ **Status**: Disponível mas com limitações
- 🌐 **Endpoint**: `https://api.coingecko.com/api/v3`
- 📊 **Rate Limit**: 10-50 requisições/minuto (free tier)
- 🔑 **Autenticação**: Opcional (API key para mais requests)
- 💰 **Custo**: Gratuito (limitado) / Pago ($129/mês)
- 🎯 **Ideal para**: Desenvolvimento, testes

**Endpoints usados:**
- `/simple/price?ids=tether,usd-coin&vs_currencies=brl`

---

### 3. **Brasil Bitcoin API** (Futuro)
- 🚧 **Status**: Planejado para implementação futura
- 🌐 **Endpoint**: `https://brasilbitcoin.com.br/api/v2`
- 📊 **Rate Limit**: 2000 weight/minuto (público)
- 🔑 **Autenticação**: **Obrigatória** (API Key + HMAC SHA256)
- 💰 **Custo**: Gratuito (requer conta)
- 🎯 **Ideal para**: Mercado brasileiro, dados locais
- ⚙️ **Requisitos**:
  - Conta na Brasil Bitcoin
  - API Key gerada
  - IP Whitelist configurado
  - Implementação de assinatura HMAC

---

## 🔧 Como Trocar de Provider

### Método 1: Variável de Ambiente (Recomendado)

Defina a variável de ambiente `COTACAO_CRYPTO_PROVIDER`:

```bash
# Usar Binance (padrão)
export COTACAO_CRYPTO_PROVIDER=binance

# Usar CoinGecko
export COTACAO_CRYPTO_PROVIDER=coingecko

# Usar Brasil Bitcoin (quando implementado)
export COTACAO_CRYPTO_PROVIDER=brasilbitcoin
```

### Método 2: Arquivo `.env`

Crie/edite o arquivo `.env` na raiz do projeto:

```env
COTACAO_CRYPTO_PROVIDER=binance
COTACAO_CRYPTO_API_TIMEOUT=10.0
```

### Método 3: Direto no Código

Edite `app/core/config.py`:

```python
crypto_provider: str = Field(
    default="binance",  # Mude aqui: "binance", "coingecko" ou "brasilbitcoin"
    description="Provider de cotações cripto",
)
```

---

## 📁 Arquitetura de Providers

```
app/infra/
├── cliente_cripto.py              # Provider CoinGecko
├── cliente_cripto_binance.py      # Provider Binance ✅
└── cliente_cripto_brasilbitcoin.py # Provider Brasil Bitcoin (futuro)

app/api/
└── cripto_rotas.py                # Factory que seleciona o provider
```

### Como Funciona o Factory Pattern

```python
def _get_crypto_provider():
    provider_type = settings.crypto_provider.lower()
    
    if provider_type == "binance":
        return HttpBinanceProvider()
    elif provider_type == "coingecko":
        return HttpCoinGeckoProvider()
    elif provider_type == "brasilbitcoin":
        return HttpBrasilBitcoinProvider()  # Implementar
    else:
        return HttpBinanceProvider()  # Default
```

---

## 🚀 Implementando Novo Provider

Para adicionar um novo provider (ex: Brasil Bitcoin):

### 1. Criar arquivo do provider

`app/infra/cliente_cripto_brasilbitcoin.py`:

```python
class HttpBrasilBitcoinProvider:
    async def buscar_usdt_brl(self) -> float:
        # Implementação específica
        pass
    
    async def buscar_usdc_brl(self) -> float:
        # Implementação específica
        pass
    
    async def buscar_ambas_brl(self) -> Dict[str, float]:
        # Implementação específica
        pass
```

### 2. Atualizar o factory

Em `app/api/cripto_rotas.py`:

```python
from app.infra.cliente_cripto_brasilbitcoin import HttpBrasilBitcoinProvider

def _get_crypto_provider():
    # ... código existente ...
    elif provider_type == "brasilbitcoin":
        return HttpBrasilBitcoinProvider(
            api_key=settings.brasilbitcoin_api_key,
            api_secret=settings.brasilbitcoin_api_secret,
            timeout=timeout
        )
```

### 3. Adicionar configurações

Em `app/core/config.py`:

```python
# Brasil Bitcoin
brasilbitcoin_api_key: str = Field(default="", description="API Key Brasil Bitcoin")
brasilbitcoin_api_secret: str = Field(default="", description="API Secret Brasil Bitcoin")
```

---

## 📊 Comparação de Performance

| Provider | Latência Média | Requests/Min | Confiabilidade |
|----------|---------------|--------------|----------------|
| Binance | ~50-150ms | 1200 | ⭐⭐⭐⭐⭐ |
| CoinGecko | ~300-500ms | 10-50 | ⭐⭐⭐ |
| Brasil Bitcoin | ~100-200ms* | 2000* | ⭐⭐⭐⭐ |

*Estimado - requer implementação e testes

---

## 🔍 Testando Providers

### Teste via cURL

```bash
# Testar endpoint
curl http://localhost:8888/cripto/ambas-brl | jq

# Verificar qual provider está ativo
curl http://localhost:8888/cripto/usdt-brl | jq '.fonte'
```

### Teste via Python

```python
import requests

response = requests.get("http://localhost:8888/cripto/ambas-brl")
data = response.json()

print(f"Fonte: {data['USDT']['fonte']}")
print(f"USDT/BRL: R$ {data['USDT']['taxa_cambio']}")
print(f"USDC/BRL: R$ {data['USDC']['taxa_cambio']}")
```

---

## ⚠️ Troubleshooting

### Erro 429 - Rate Limit

**CoinGecko**: Reduza frequência de refresh ou use API key paga
**Binance**: Muito raro, verifique se não há loop infinito
**Brasil Bitcoin**: Verifique weight limits na documentação

### Timeout

Aumente o timeout em `.env`:
```env
COTACAO_CRYPTO_API_TIMEOUT=20.0
```

### Provider não reconhecido

Cai no default (Binance). Verifique:
- Nome correto do provider
- Variável de ambiente configurada
- Restart do servidor

---

## 📝 Changelog

- **v1.0** (18/11/2025): Implementado Binance como provider padrão
- **v0.9** (18/11/2025): CoinGecko implementado (com rate limit issues)
- **Futuro**: Brasil Bitcoin API planejada

---

## 💡 Recomendações

### Desenvolvimento
- Use **CoinGecko** ou **Binance**
- Sem necessidade de API keys

### Produção
- Use **Binance** (atual)
- Considere **Brasil Bitcoin** se precisar de:
  - Dados específicos do mercado BR
  - Trading automatizado
  - Liquidez local

### Migração Futura
Quando migrar para Brasil Bitcoin:
1. Criar conta e gerar API Key
2. Implementar provider
3. Configurar IP whitelist
4. Testar em staging
5. Mudar variável de ambiente
6. Deploy
