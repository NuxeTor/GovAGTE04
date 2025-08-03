#!/usr/bin/env python3
"""
Script otimizado para rodar o servidor Flask no Replit
"""
import os
from app import app

if __name__ == '__main__':
    # Configuração específica para Replit
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print(f"🚀 Iniciando servidor Flask em {host}:{port}")
    print(f"🌐 Preview disponível em: http://{host}:{port}")
    
    # Rodar com configurações otimizadas para Replit
    app.run(
        host=host,
        port=port,
        debug=True,
        threaded=True,
        use_reloader=True
    )