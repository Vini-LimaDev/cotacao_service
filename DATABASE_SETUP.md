# Configuração do Banco de Dados PostgreSQL

## 📋 Pré-requisitos

Certifique-se de ter o PostgreSQL instalado em sua máquina.

### Instalar PostgreSQL no Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Verificar se está rodando:
```bash
sudo systemctl status postgresql
```

## 🛠️ Configuração Inicial

### 1. Acessar o PostgreSQL como superusuário
```bash
sudo -u postgres psql
```

### 2. Criar banco de dados e usuário
```sql
-- Criar usuário
CREATE USER cotacao_user WITH PASSWORD 'cotacao_pass';

-- Criar banco de dados
CREATE DATABASE cotacao_db;

-- Dar permissões ao usuário
GRANT ALL PRIVILEGES ON DATABASE cotacao_db TO cotacao_user;

-- Sair do psql
\q
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (cotacao_service/):

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais reais:
```env
COTACAO_DATABASE_URL=postgresql://cotacao_user:cotacao_pass@localhost:5432/cotacao_db
COTACAO_SECRET_KEY=sua-chave-secreta-muito-segura-aqui-123456789
COTACAO_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**IMPORTANTE:** Nunca commite o arquivo `.env` no Git!

### 4. Ativar ambiente virtual
```bash
source venv/bin/activate
```

### 5. Executar migrações do Alembic

Criar a primeira migração (tabela de usuários):
```bash
alembic revision --autogenerate -m "create users table"
```

Aplicar as migrações no banco:
```bash
alembic upgrade head
```

### 6. Verificar se a tabela foi criada
```bash
sudo -u postgres psql -d cotacao_db -c "\dt"
```

Você deve ver a tabela `users` listada.

## 🔄 Comandos Úteis do Alembic

```bash
# Ver histórico de migrações
alembic history

# Ver migração atual
alembic current

# Reverter última migração
alembic downgrade -1

# Aplicar todas migrações
alembic upgrade head

# Criar nova migração
alembic revision --autogenerate -m "descrição da alteração"
```

## 🧪 Testar conexão com banco

Você pode testar se está tudo funcionando rodando este comando Python:
```bash
python -c "from app.infra.database import engine; print('Conectado ao banco:', engine.url)"
```

## ❓ Troubleshooting

### Erro: "could not connect to server"
- Verifique se o PostgreSQL está rodando: `sudo systemctl start postgresql`

### Erro: "password authentication failed"
- Verifique suas credenciais no arquivo `.env`
- Recrie o usuário no PostgreSQL

### Erro: "database does not exist"
- Crie o banco de dados conforme passo 2

### Erro de permissão no PostgreSQL 15+
Se você estiver usando PostgreSQL 15 ou superior, pode precisar dar permissões adicionais:
```sql
sudo -u postgres psql
\c cotacao_db
GRANT ALL ON SCHEMA public TO cotacao_user;
```

## 🚀 Próximos Passos

Após configurar o banco:
1. Implementar rotas de autenticação (login, registro)
2. Criar middleware de proteção de rotas
3. Integrar frontend com autenticação
