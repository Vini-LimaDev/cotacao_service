# 💱 Serviço de Cotação de Moedas

Sistema completo de cotação de moedas com backend em FastAPI e frontend em React, utilizando cache em memória e integração com a API Frankfurter.

## 📦 Estrutura do Projeto

```
📦 cotacao_service
 ┣ 📂 app                       # Backend FastAPI
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 main.py                 # Ponto de entrada FastAPI
 ┃ ┃
 ┃ ┣ 📂 api                     # Camada de apresentação (rotas)
 ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┗ 📜 cotacao_rotas.py     # Endpoints REST da API
 ┃ ┃
 ┃ ┣ 📂 core                    # Configurações centrais
 ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┗ 📜 config.py             # Configurações da aplicação
 ┃ ┃
 ┃ ┣ 📂 domain                  # Camada de domínio (regras de negócio)
 ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┣ 📜 models.py             # Modelos de domínio (Cotacao)
 ┃ ┃ ┗ 📜 portas.py             # Interfaces/contratos (Ports)
 ┃ ┃
 ┃ ┗ 📂 infra                   # Camada de infraestrutura (adaptadores)
 ┃   ┣ 📜 __init__.py
 ┃   ┣ 📜 cache.py              # Sistema de cache em memória
 ┃   ┣ 📜 cliente_externo.py   # Cliente HTTP para API Frankfurter
 ┃   ┗ 📜 cotacao_repo.py      # Repositório com cache
 ┃
 ┣ 📂 cotacao-frontend          # Frontend React + Vite
 ┃ ┣ 📜 index.html              # Estrutura HTML base
 ┃ ┣ 📜 package.json            # Dependências do frontend
 ┃ ┣ 📜 vite.config.js          # Configuração do Vite
 ┃ ┣ 📜 eslint.config.js        # Configuração do ESLint
 ┃ ┣ 📜 README.md               # Documentação do frontend
 ┃ ┃
 ┃ ┣ 📂 public                  # Arquivos estáticos públicos
 ┃ ┃
 ┃ ┗ 📂 src                     # Código-fonte do frontend
 ┃   ┣ 📜 main.jsx              # Ponto de entrada React
 ┃   ┣ 📜 App.jsx               # Componente principal
 ┃   ┣ 📜 App.css               # Estilos do componente
 ┃   ┣ 📜 index.css             # Estilos globais
 ┃   ┗ 📂 assets                # Recursos (imagens, ícones, etc.)
 ┃
 ┣ 📂 .vscode                   # Configurações do VS Code
 ┃ ┗ 📜 settings.json
 ┃
 ┣ 📜 requirements.txt          # Dependências Python
 ┣ 📜 .gitignore
 ┗ 📜 README.md                 # Este arquivo
```

## 🏗️ Arquitetura

O projeto segue uma **arquitetura hexagonal (ports and adapters)** no backend:

### 🧠 Backend (FastAPI)

- **`app/api/`**: Camada de apresentação - define os endpoints REST
- **`app/core/`**: Configurações centralizadas da aplicação
- **`app/domain/`**: Núcleo da aplicação com regras de negócio
  - `models.py`: Entidades de domínio
  - `portas.py`: Interfaces/contratos para inversão de dependência
- **`app/infra/`**: Implementações concretas dos adaptadores
  - `cache.py`: Sistema de cache em memória com TTL
  - `cliente_externo.py`: Integração com API externa (Frankfurter)
  - `cotacao_repo.py`: Repositório que combina cache + API externa

### 💻 Frontend (React + Vite)

- **Componente único**: Interface simples e responsiva
- **Funcionalidades**:
  - Seleção de moedas de origem e destino
  - Busca automática de cotações
  - Conversão bidirecional de valores
  - Notificações toast de sucesso

---
## 🚀 Como Executar

### Pré-requisitos

- Python 3.10+
- Node.js 16+
- npm ou yarn

### Backend

```bash
# Instalar dependências
cd cotacao_service
pip install -r requirements.txt

# Executar o servidor (porta 9876)

uvicorn app.main:app --port 9876 --reload
```

### Frontend

```bash
# Navegar para a pasta do frontend
cd cotacao-frontend

# Abre o ambiente virtual
source .venv/bin/activate

# Instalar dependências
npm install

# Executar o servidor de desenvolvimento (porta 5173)
npm run dev
```

## 🔌 Endpoints da API

### `GET /health`
Healthcheck da aplicação

**Resposta:**
```json
{
  "status": "ok"
}
```

### `GET /cotacao`
Obtém a cotação entre duas moedas

**Parâmetros:**
- `moeda_origem` (string): Código da moeda de origem (ex: USD)
- `moeda_destino` (string): Código da moeda de destino (ex: BRL)

**Resposta:**
```json
{
  "moeda_origem": "USD",
  "moeda_destino": "BRL",
  "taxa_cambio": 5.25,
  "data_cotacao": "2025-11-17T10:30:00",
  "fonte": "cache"
}
```
## ⚙️ Configuração

As configurações podem ser ajustadas em `app/core/config.py`:

- **`cache_ttl_seconds`**: Tempo de vida do cache (padrão: 300s)
- **`frankfurter_base_url`**: URL da API Frankfurter
- **`frankfurter_timeout_seconds`**: Timeout das requisições HTTP

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e de alta performance
- **Pydantic**: Validação de dados e configurações
- **httpx**: Cliente HTTP assíncrono
- **uvicorn**: Servidor ASGI

### Frontend
- **React 18**: Biblioteca para interfaces de usuário
- **Vite**: Build tool e dev server rápido
- **ESLint**: Linter para qualidade de código

## 📝 Funcionalidades

- ✅ Cache em memória com TTL configurável
- ✅ Integração com API Frankfurter
- ✅ Validação de códigos de moeda
- ✅ CORS configurado para desenvolvimento
- ✅ Interface responsiva e moderna
- ✅ Conversão bidirecional de valores
- ✅ Notificações de sucesso
- ✅ Atualização automática ao trocar moedas

## 🔄 Fluxo de Dados

1. Frontend solicita cotação via endpoint `/cotacao`
2. Backend verifica se existe no cache
3. Se não existir ou estiver expirado, busca na API Frankfurter
4. Armazena no cache e retorna ao frontend
5. Frontend exibe a cotação e permite conversão de valores
---




**API Externa utilizada**: [Frankfurter](https://www.frankfurter.app/) - API gratuita de taxas de câmbio
