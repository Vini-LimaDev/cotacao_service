#!/usr/bin/env bash
# Build script para o Render

set -e

echo "🔧 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️  Rodando migrações do banco de dados..."
alembic upgrade head

echo "✅ Build concluído!"
