#!/usr/bin/env python3
"""
Script de inicialização robusta para o servidor Flask
"""
import os
import signal
import time
import subprocess
import sys

def kill_port_processes():
    """Mata todos os processos usando a porta 5000"""
    try:
        # Mata processos python relacionados
        subprocess.run(['pkill', '-9', '-f', 'python.*app'], check=False)
        subprocess.run(['pkill', '-9', '-f', 'gunicorn'], check=False)
        subprocess.run(['pkill', '-9', '-f', 'flask'], check=False)
        time.sleep(2)
        print("✅ Processos anteriores removidos")
    except Exception as e:
        print(f"Aviso ao limpar processos: {e}")

def start_flask_server():
    """Inicia o servidor Flask diretamente"""
    from app import app
    
    print("🚀 Iniciando servidor Flask...")
    print("🌐 Preview disponível em: http://0.0.0.0:5000")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )

if __name__ == '__main__':
    kill_port_processes()
    start_flask_server()