#!/usr/bin/env python
"""
Script para executar a aplicação FastAPI
Uso: python run.py
Ou com uvicorn diretamente: uvicorn main:app --reload
"""

import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Configurações
    HOST = "127.0.0.1"
    PORT = 8000
    RELOAD = True  # Auto-reload ao detectar mudanças
    
    print("=" * 60)
    print("🚀 Iniciando API Cybersecurity Threats")
    print("=" * 60)
    print(f"📍 Host: {HOST}")
    print(f"📍 Port: {PORT}")
    print(f"📚 Documentação: http://{HOST}:{PORT}/docs")
    print("=" * 60)
    
    # Executar o servidor
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level="info"
    )
