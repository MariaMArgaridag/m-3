# 🛑 Como Parar e Reiniciar o Servidor

## Parar o Servidor

Se você deixar o servidor rodando em um terminal:

### Opção 1: Pressionar CTRL+C
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Simplesmente pressione **CTRL + C** no terminal onde o servidor está rodando.

Você verá:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process
INFO:     Stopping reloader process
```

### Opção 2: Fechar o Terminal
Se executou em um novo processo, simplesmente feche a janela do terminal.

### Opção 3: Matar Processo (PowerShell)
Se precisar forçar a parada:

```powershell
# Listar todos os processos Python rodando
Get-Process python

# Matar o processo específico (substitua XXXXX pelo PID)
Stop-Process -Id XXXXX -Force

# Ou matar todos os Python (cuidado!)
Stop-Process -Name python -Force
```

---

## Reiniciar o Servidor

### Opção 1: Mesmo Terminal
Após parar com CTRL+C, execute novamente:
```powershell
python run.py
```

### Opção 2: Novo Terminal
```powershell
# Abrir novo PowerShell
cd "c:\Users\tatia\Desktop\Docs\Estudos\UPskill\Sistemas Cliente Servidor\m-3"
.\M3Venv\Scripts\Activate.ps1
python run.py
```

### Opção 3: Sem Auto-reload
Se quiser mais performance (mas não recarregar ao salvar arquivos):
```powershell
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Opção 4: Porta Diferente
Se a porta 8000 estiver em uso:
```powershell
python run.py  # Editar run.py para mudar porta
# Ou diretamente:
uvicorn main:app --host 127.0.0.1 --port 8001
```

---

## Verificar se Está Rodando

```powershell
# Testar via curl
curl http://127.0.0.1:8000/health

# Ou abrir no navegador
Start-Process "http://127.0.0.1:8000/docs"
```

---

## Troubleshooting

### Erro: "Port 8000 already in use"

```powershell
# Encontrar e matar o processo na porta 8000
Get-NetTCPConnection -LocalPort 8000 | Select OwningProcess
Stop-Process -Id XXXXX -Force
```

### Erro: "Address already in use"

```powershell
# Aguarde alguns segundos e tente novamente
# Às vezes a porta fica "aberta" por alguns momentos

Start-Sleep -Seconds 5
python run.py
```

### Verificar se MySQL está rodando

```powershell
# Testar conexão
curl "http://127.0.0.1:8000/health"

# Se "Connection refused", MySQL pode estar desligado
```

---

## Dicas Úteis

### Manter Servidor Rodando
```powershell
# Usar Start-Job para rodar em background
Start-Job -ScriptBlock {
    cd "c:\Users\tatia\Desktop\Docs\Estudos\UPskill\Sistemas Cliente Servidor\m-3"
    .\M3Venv\Scripts\Activate.ps1
    python run.py
}
```

### Ver Logs Mais Detalhados
Editar `run.py`:
```python
uvicorn.run(
    "main:app",
    host=HOST,
    port=PORT,
    reload=RELOAD,
    log_level="debug"  # Mudar para "debug" para mais logs
)
```

### Desabilitar Auto-reload
Editar `run.py`:
```python
uvicorn.run(
    "main:app",
    host=HOST,
    port=PORT,
    reload=False  # Desabilitar recarregamento automático
)
```

---

✅ Tudo pronto! O servidor pode ser facilmente parado e reiniciado.
