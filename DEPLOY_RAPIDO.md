# 🚀 Deploy Rápido - Render.com

## ✅ Arquivos Criados para Deploy

Criei os seguintes arquivos para facilitar o deploy:

- ✅ `render.yaml` - Configuração automática do Render
- ✅ `build.sh` - Script de build do backend
- ✅ `runtime.txt` - Versão do Python
- ✅ `.env.example` - Exemplo de variáveis de ambiente
- ✅ `DEPLOY.md` - Guia completo de deploy

## 🎯 Próximos Passos (VOCÊ FAZ)

### 1️⃣ Enviar código pro GitHub

```bash
cd /home/vinicius_lima/api_cotacao/cotacao_service
git add .
git commit -m "Preparando para deploy no Render"
git push origin version-oficial
```

### 2️⃣ Criar conta no Render

1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Faça login com GitHub
4. Autorize o Render

### 3️⃣ Fazer Deploy Automático

1. No Render, clique em **"New +"** → **"Blueprint"**
2. Selecione seu repositório `cotacao_service`
3. O Render vai detectar o `render.yaml`
4. Clique em **"Apply"**
5. Aguarde 5-10 minutos ☕

### 4️⃣ Pronto! 🎉

Seu site estará no ar em:
- Frontend: `https://cotacao-frontend.onrender.com`
- API: `https://cotacao-api.onrender.com`

---

## ⚠️ IMPORTANTE

**Plano Grátis**: O backend "hiberna" após 15min sem uso. A primeira requisição após hibernar demora ~30 segundos para "acordar".

**Upgrade ($7/mês)**: Se quiser evitar hibernação, upgrade para o plano pago.

---

## 🆘 Problemas?

Leia o guia completo em: `DEPLOY.md`

**Bom deploy! 🚀**
