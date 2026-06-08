#!/bin/bash
# PriceWatch — Script de início rápido
# Musical Presentes

echo ""
echo "🎸 PriceWatch — Musical Presentes"
echo "=================================="

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale em https://python.org"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Instala dependências
echo ""
echo "📦 Instalando dependências..."
cd "$(dirname "$0")/backend"
pip install -r requirements.txt -q

echo ""
echo "🚀 Iniciando servidor PriceWatch..."
echo "   Dashboard: abra frontend/index.html no navegador"
echo "   API:       http://localhost:5000/api"
echo ""
echo "   Pressione Ctrl+C para parar"
echo ""

python3 server.py
