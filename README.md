# 🔒 Cybersecurity Threats REST API

Uma API REST completa com arquitetura em 4 camadas para gerenciar dados de ameaças de cibersegurança.

## 📋 Estrutura do Projeto

```
├── main.py                 # Camada 1: Apresentação (Rotas FastAPI)
├── models.py              # Camada 3: Persistência (Modelos ORM SQLAlchemy)
├── services.py            # Camada 2: Negócios (Lógica de aplicação)
├── database.py            # Configuração do banco de dados
├── run.py                 # Script para executar a aplicação
├── .env                   # Variáveis de ambiente (configuração do BD)
└── cybersecurity_threats.sql  # Schema do banco de dados
```

## 🏗️ Arquitetura em 4 Camadas

### Camada 1: Apresentação (`main.py`)
- Rotas HTTP (endpoints)
- Validação de entrada (Pydantic)
- Respostas estruturadas (OpenAPI/Swagger)

### Camada 2: Negócios (`services.py`)
- Lógica de aplicação
- CRUD operations
- Estatísticas e consultas complexas
- Validações de domínio

### Camada 3: Persistência (`models.py`)
- Modelos SQLAlchemy (ORM)
- Mapeamento objeto-relacional
- Relacionamentos entre tabelas

### Camada 4: Base de Dados
- MySQL com tabelas: `Attack_Types`, `Defense_Mechanisms`, `Security_Vulnerabilities`, `Target_Industries`, `Attack_Sources`, `global_cyber_threats`

## 🚀 Como Executar

### 1. Preparar o Ambiente

#### Windows (PowerShell)
```powershell
# Ativar ambiente virtual
.\M3Venv\Scripts\Activate.ps1

# Instalar dependências (se necessário)
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv
```

#### Linux/Mac (Terminal)
```bash
source M3Venv/bin/activate
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv
```

### 2. Configurar o Banco de Dados

Edite o arquivo `.env` com suas credenciais MySQL:
```
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=cybersecurity_threats
```

### 3. Executar a Aplicação

```bash
python run.py
```

Ou diretamente com uvicorn:
```bash
uvicorn main:app --reload
```

A API estará disponível em: **http://127.0.0.1:8000**

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

## 📡 Endpoints Disponíveis

### Health Check
- `GET /health` - Verificar status da API

### Attack Types (Tipos de Ataque)
- `GET /attacks` - Listar todos
- `GET /attacks/{id}` - Obter por ID
- `POST /attacks` - Criar novo
- `PUT /attacks/{id}` - Atualizar
- `DELETE /attacks/{id}` - Deletar
- `GET /attacks/stats/all` - Estatísticas

### Defense Mechanisms (Mecanismos de Defesa)
- `GET /defenses` - Listar todos
- `GET /defenses/{id}` - Obter por ID
- `POST /defenses` - Criar novo
- `PUT /defenses/{id}` - Atualizar
- `DELETE /defenses/{id}` - Deletar
- `GET /defenses/stats/all` - Estatísticas

### Vulnerabilities (Vulnerabilidades)
- `GET /vulnerabilities` - Listar todos
- `GET /vulnerabilities/{id}` - Obter por ID
- `POST /vulnerabilities` - Criar novo
- `PUT /vulnerabilities/{id}` - Atualizar
- `DELETE /vulnerabilities/{id}` - Deletar
- `GET /vulnerabilities/stats/all` - Estatísticas

### Incidents (Incidentes)
- `GET /incidents` - Listar todos (com filtros opcionais: `?year=2020&country=Brazil`)
- `GET /incidents/{id}` - Obter por ID
- `POST /incidents` - Criar novo
- `PUT /incidents/{id}` - Atualizar
- `DELETE /incidents/{id}` - Deletar
- `GET /incidents/stats/all` - Estatísticas

## 📝 Exemplos de Uso

### Criar um tipo de ataque
```bash
curl -X POST "http://127.0.0.1:8000/attacks" \
  -H "Content-Type: application/json" \
  -d '{"type": "Zero-Day"}'
```

### Listar todos os tipos de ataque
```bash
curl "http://127.0.0.1:8000/attacks"
```

### Obter incidentes de um país específico
```bash
curl "http://127.0.0.1:8000/incidents?country=Brazil"
```

### Atualizar um mecanismo de defesa
```bash
curl -X PUT "http://127.0.0.1:8000/defenses/1" \
  -H "Content-Type: application/json" \
  -d '{"mechanism": "Advanced Firewall"}'
```

## ✅ Checklist de Funcionamento

- [x] Camada 1: Apresentação (Rotas FastAPI)
- [x] Camada 2: Serviços (Lógica de negócios)
- [x] Camada 3: Modelos ORM (SQLAlchemy)
- [x] Camada 4: Banco de Dados (MySQL)
- [x] Documentação OpenAPI (Swagger)
- [x] CRUD completo para todos os serviços
- [x] Estatísticas e filtros

## 🐛 Troubleshooting

### Erro: "Connection refused"
- Certifique-se de que MySQL está rodando
- Verifique as credenciais no arquivo `.env`

### Erro: "Table doesn't exist"
- A aplicação cria as tabelas automaticamente na primeira execução
- Se precisar resetar, execute o arquivo SQL: `cybersecurity_threats.sql`

### Erro: "ModuleNotFoundError"
- Ative o ambiente virtual
- Instale as dependências: `pip install -r requirements.txt`

## 📦 Dependências

```
fastapi==0.128.0
uvicorn==0.40.0
sqlalchemy==2.0.45
pymysql==1.1.2
python-dotenv==1.2.1
pydantic==2.12.5
```

## 🎓 Aprendizados

Este projeto demonstra:
- Arquitetura em camadas (Clean Architecture)
- API REST com FastAPI
- ORM com SQLAlchemy
- Boas práticas de segurança (variáveis de ambiente)
- Documentação automática com OpenAPI
- Tratamento de erros HTTP
- Validação de dados com Pydantic

---

**Desenvolvido com ❤️ para o curso de Sistemas Cliente-Servidor**
