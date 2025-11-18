# 🚀 Guia de Deploy no Render

Este guia vai te ajudar a colocar sua aplicação no ar usando o Render.com (grátis!).

## 📋 Pré-requisitos

1. ✅ Conta no GitHub
2. ✅ Código enviado para o GitHub
3. ✅ Conta no Render.com (criar em https://render.com)

---

## 🎯 Passo a Passo

### 1. Preparar o Repositório GitHub

Se ainda não fez push do código:

```bash
cd /home/vinicius_lima/api_cotacao/cotacao_service
git add .
git commit -m "Preparando para deploy no Render"
git push origin main
```

### 2. Criar Conta no Render

1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Faça login com sua conta GitHub
4. Autorize o Render a acessar seus repositórios

### 3. Fazer Deploy via Blueprint (Método Automático)

#### Opção A: Deploy Automático com render.yaml

1. No painel do Render, clique em **"New +"** → **"Blueprint"**
2. Conecte seu repositório `cotacao_service`
3. O Render vai detectar o arquivo `render.yaml` automaticamente
4. Clique em **"Apply"**
5. Aguarde o deploy (5-10 minutos)

✅ **Pronto! Seu app estará no ar!**

---

#### Opção B: Deploy Manual (se preferir controle total)

##### 3.1. Criar o Banco de Dados PostgreSQL

1. No Render Dashboard, clique em **"New +"** → **"PostgreSQL"**
2. Preencha:
   - **Name**: `cotacao-db`
   - **Database**: `cotacao_db`
   - **User**: `cotacao_user`
   - **Region**: Oregon (US West)
   - **Plan**: Free
3. Clique em **"Create Database"**
4. Aguarde ~2 minutos
5. **Copie a "Internal Database URL"** (vamos usar depois)

##### 3.2. Criar o Backend (API)

1. Clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub
3. Preencha:
   - **Name**: `cotacao-api`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `.` (raiz)
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. Clique em **"Advanced"** e adicione as variáveis de ambiente:

   ```
   COTACAO_DATABASE_URL = [Cole a Internal Database URL aqui]
   COTACAO_SECRET_KEY = [Gere um token aleatório - pode usar https://www.uuidgenerator.net/]
   COTACAO_FRANKFURTER_TIMEOUT_SECONDS = 15
   COTACAO_CRYPTO_PROVIDER = binance
   PYTHON_VERSION = 3.11.0
   ```

5. Clique em **"Create Web Service"**
6. Aguarde o build (~5 minutos)
7. **Copie a URL do serviço** (ex: `https://cotacao-api.onrender.com`)

##### 3.3. Criar o Frontend

1. Clique em **"New +"** → **"Static Site"**
2. Conecte o mesmo repositório
3. Preencha:
   - **Name**: `cotacao-frontend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `cotacao-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

4. Clique em **"Advanced"** e adicione:

   ```
   VITE_API_BASE_URL = [Cole a URL do backend aqui, ex: https://cotacao-api.onrender.com]
   ```

5. Clique em **"Create Static Site"**
6. Aguarde o build (~3 minutos)

##### 3.4. Atualizar CORS no Backend

1. Volte ao serviço **cotacao-api**
2. Vá em **Environment** → **Environment Variables**
3. Adicione:
   ```
   FRONTEND_URL = [URL do seu frontend, ex: https://cotacao-frontend.onrender.com]
   ```
4. Clique em **"Save Changes"**
5. O backend vai fazer redeploy automaticamente

---

## 🎉 Pronto!

Seu site estará disponível em:
- **Frontend**: `https://cotacao-frontend.onrender.com`
- **Backend API**: `https://cotacao-api.onrender.com`

Acesse o frontend e teste! 🚀

---

## ⚠️ Limitações do Plano Grátis

- ⏸️ Backend hiberna após 15 minutos sem uso
- ⏰ Primeira requisição após hibernar demora ~30 segundos
- 📊 Banco de dados PostgreSQL grátis por 90 dias
- 💾 500MB de armazenamento no banco

**💡 Dica**: Se quiser evitar a hibernação, upgrade para o plano pago ($7/mês) ou use um serviço de "ping" para manter o backend ativo.

---

## 🔧 Troubleshooting

### Backend não inicia?
- Verifique os logs: Dashboard → seu serviço → Logs
- Confirme que todas as variáveis de ambiente estão corretas
- Verifique se o `build.sh` tem permissão de execução

### Frontend com erro 404 na API?
- Confirme que `VITE_API_BASE_URL` aponta para o backend correto
- Verifique se adicionou `FRONTEND_URL` no backend

### Banco de dados com erro de conexão?
- Use a **Internal Database URL**, não a External
- Formato: `postgresql://user:password@host/database`

---

## 📚 Recursos

- [Documentação do Render](https://render.com/docs)
- [Deploy Python no Render](https://render.com/docs/deploy-fastapi)
- [Deploy Static Site](https://render.com/docs/deploy-vite)

---

## 🆘 Precisa de Ajuda?

Se algo der errado:
1. Verifique os logs no Render Dashboard
2. Confira se todas as variáveis de ambiente estão corretas
3. Certifique-se de que o código está atualizado no GitHub

**Bom deploy! 🚀**
