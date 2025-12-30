# 🚀 GUIA RÁPIDO - COMO COMEÇAR

## ⚡ 3 Passos para Rodar

### Passo 1: Ativar Ambiente Virtual
```powershell
cd "c:\Users\tatia\Desktop\Docs\Estudos\UPskill\Sistemas Cliente Servidor\m-3"
.\M3Venv\Scripts\Activate.ps1
```

### Passo 2: Verificar `.env`
Abra o arquivo `.env` e confirme:
```
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha_aqui
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=cybersecurity_threats
```

### Passo 3: Executar
```powershell
python run.py
```

✅ Pronto! A API está rodando em http://127.0.0.1:8000

---

## 📚 Acessar a Documentação

- **Swagger (Interativo)**: http://127.0.0.1:8000/docs
- **ReDoc (Leitura)**: http://127.0.0.1:8000/redoc

---

## 🧪 Testar a API (Novo Terminal)

```powershell
# Com venv ativado
python test_api.py
```

---

## 📡 Exemplos Rápidos (PowerShell)

### Listar todos os ataques
```powershell
curl "http://127.0.0.1:8000/attacks" | ConvertFrom-Json | Format-List
```

### Listar incidentes do Brasil
```powershell
curl "http://127.0.0.1:8000/incidents?country=Brazil" | ConvertFrom-Json | Format-List
```

### Ver estatísticas
```powershell
curl "http://127.0.0.1:8000/incidents/stats/all" | ConvertFrom-Json | Format-List
```

### Criar novo ataque
```powershell
$body = @{ type = "Nova Ameaça" } | ConvertTo-Json
curl -X POST "http://127.0.0.1:8000/attacks" `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | ConvertFrom-Json | Format-List
```

---

## 📂 Estrutura Importante

```
m-3/
├── main.py              # Rotas (Camada 1)
├── services.py          # Lógica (Camada 2)
├── models.py            # ORM (Camada 3)
├── schemas.py           # Validação
├── database.py          # Conexão
├── .env                 # Configuração
├── run.py               # Executar
├── test_api.py          # Testes
├── README.md            # Documentação
└── IMPLEMENTACAO.md     # Resumo técnico
```

---

## ❓ Problemas Comuns

| Problema | Solução |
|----------|---------|
| `Connection refused` | MySQL não está rodando / verificar `.env` |
| `ModuleNotFoundError` | Ativar venv: `.\M3Venv\Scripts\Activate.ps1` |
| `Port 8000 em uso` | Parar outro processo ou usar porta diferente |
| `SQL errors` | Executar `cybersecurity_threats.sql` no MySQL |

---

## 🎯 Funcionalidades

✅ CRUD completo (Create, Read, Update, Delete)
✅ Filtros (ano, país)
✅ Estatísticas (perdas totais, usuários, tempo)
✅ Validação automática
✅ Documentação interativa
✅ 4 Camadas de arquitetura

---

**Tudo pronto! Boa sorte com o projeto!** 🎓
