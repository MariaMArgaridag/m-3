# Documentação Técnica — Cyber Threats API

## Tecnologias Utilizadas

- **Python 3.13**
- **Flask** — Framework web
- **pip** — Gerenciador de dependências
- **MySQL** — Banco de dados
- **Virtual Environment (venv)** — Isolamento de dependências
- **Variáveis de ambiente (.env)** — Configuração segura
- **OpenAPI 3** — Documentação da API (openapi.yaml)

---

## Estrutura do Projeto

```
app/
├── controller/     # Rotas HTTP e endpoints
├── service/        # Regras de negócio e lógica da aplicação
├── repository/     # Acesso e manipulação do banco de dados
├── database.py     # Configuração e conexão com o MySQL
└── main.py         # Inicialização da aplicação Flask
openapi.yaml        # Documentação OpenAPI da API
.env                # Variáveis de ambiente
venv/               # Ambiente virtual Python
```

---

## Configuração do Ambiente

### 1. Criar e ativar o ambiente virtual

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python3 -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Configuração do Banco de Dados

Crie o arquivo `.env` na raiz do projeto com as seguintes variáveis, adaptando para seu banco de dados:

```env
DB_HOST=localhost
DB_USERNAME=root
DB_PASSWORD=''
DB_DATABASE=flask
```

---

## Executar o Projeto

Com o ambiente virtual ativado, execute:

```bash
python app/main.py
```

A API ficará disponível em:

```
http://localhost:5000
```
