# 🏛️ ARQUITETURA DO PROJETO

## Diagrama em Camadas

```
┌──────────────────────────────────────────────────────────┐
│                    CLIENTE (Browser/API Client)          │
│                                                          │
│           http://127.0.0.1:8000/docs (Swagger)         │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│           CAMADA 1: APRESENTAÇÃO (main.py)              │
│                                                          │
│  • FastAPI Application                                  │
│  • HTTP Routes (GET, POST, PUT, DELETE)                │
│  • Request/Response Validation (Pydantic)              │
│  • Error Handling (HTTP Status Codes)                  │
│  • OpenAPI 3.0 Documentation                           │
│                                                          │
│  Endpoints:                                             │
│  ├── GET/POST    /attacks                               │
│  ├── GET/POST    /defenses                              │
│  ├── GET/POST    /vulnerabilities                       │
│  ├── GET/POST    /incidents                             │
│  └── GET         /health                                │
└──────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │   DEPENDENCY INJECTION (db: Session)   │
        └─────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│        CAMADA 2: NEGÓCIOS/SERVIÇOS (services.py)        │
│                                                          │
│  • CRUD Operations                                      │
│  • Business Logic                                       │
│  • Data Validation                                      │
│  • Statistics & Analytics                              │
│  • Filtering & Sorting                                 │
│                                                          │
│  Serviços:                                              │
│  ├── list_attack_types()                                │
│  ├── get_attack_type(id)                                │
│  ├── create_attack_type(data)                           │
│  ├── update_attack_type(id, data)                       │
│  ├── delete_attack_type(id)                             │
│  ├── attack_types_stats()                               │
│  │                                                      │
│  ├── list_defense_mechanisms()                          │
│  ├── get_defense_mechanism(id)                          │
│  ├── create_defense_mechanism(data)                     │
│  ├── update_defense_mechanism(id, data)                 │
│  ├── delete_defense_mechanism(id)                       │
│  ├── defense_mechanisms_stats()                         │
│  │                                                      │
│  ├── list_vulnerabilities()                             │
│  ├── get_vulnerability(id)                              │
│  ├── create_vulnerability(data)                         │
│  ├── update_vulnerability(id, data)                     │
│  ├── delete_vulnerability(id)                           │
│  ├── vulnerabilities_stats()                            │
│  │                                                      │
│  ├── list_incidents(year, country)                      │
│  ├── get_incident(id)                                   │
│  ├── create_incident(data)                              │
│  ├── update_incident(id, data)                          │
│  ├── delete_incident(id)                                │
│  └── incidents_stats()                                  │
└──────────────────────────────────────────────────────────┘
                              ↓
            ┌────────────────────────────────┐
            │   SQLAlchemy Session/Connection  │
            │   (database.py)                │
            └────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│      CAMADA 3: PERSISTÊNCIA/ORM (models.py)             │
│                                                          │
│  SQLAlchemy Models (Object-Relational Mapping):        │
│                                                          │
│  ├── AttackType                                         │
│  │   └── Maps to: Attack_Types table                    │
│  │                                                      │
│  ├── DefenseMechanism                                   │
│  │   └── Maps to: Defense_Mechanisms table              │
│  │                                                      │
│  ├── SecurityVulnerability                              │
│  │   └── Maps to: Security_Vulnerabilities table        │
│  │                                                      │
│  ├── TargetIndustry                                     │
│  │   └── Maps to: Target_Industries table               │
│  │                                                      │
│  ├── AttackSource                                       │
│  │   └── Maps to: Attack_Sources table                  │
│  │                                                      │
│  └── GlobalCyberThreat                                  │
│      └── Maps to: global_cyber_threats table            │
│          with Foreign Keys to:                          │
│          ├── Attack_Types (attack_type)                 │
│          ├── Target_Industries (target_industry)        │
│          ├── Attack_Sources (attack_source)             │
│          ├── Security_Vulnerabilities (...)             │
│          └── Defense_Mechanisms (...)                   │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│          CAMADA 4: BASE DE DADOS (MySQL)                │
│                                                          │
│  Database: cybersecurity_threats                        │
│                                                          │
│  Tables:                                                │
│  ├── Attack_Types (6 registros)                         │
│  │   ├── Id (PK)                                        │
│  │   └── Type                                           │
│  │                                                      │
│  ├── Defense_Mechanisms (6 registros)                   │
│  │   ├── Id (PK)                                        │
│  │   └── Mechanism                                      │
│  │                                                      │
│  ├── Security_Vulnerabilities (? registros)             │
│  │   ├── Id (PK)                                        │
│  │   └── vulnerability                                  │
│  │                                                      │
│  ├── Target_Industries (7 registros)                    │
│  │   ├── Id (PK)                                        │
│  │   └── industry                                       │
│  │                                                      │
│  ├── Attack_Sources (4 registros)                       │
│  │   ├── Id (PK)                                        │
│  │   └── Source                                         │
│  │                                                      │
│  └── global_cyber_threats (238+ registros)              │
│      ├── Id (PK)                                        │
│      ├── Country                                        │
│      ├── Year                                           │
│      ├── Attack Type (FK)                               │
│      ├── Target Industry (FK)                           │
│      ├── Financial Loss                                 │
│      ├── Affected Users                                 │
│      ├── Attack Source (FK)                             │
│      ├── Security Vulnerability Type (FK)              │
│      ├── Defense Mechanism Used (FK)                    │
│      └── Incident Resolution Time                       │
└──────────────────────────────────────────────────────────┘
                              ↓
            ┌────────────────────────────────┐
            │    MySQL Server (localhost)    │
            │    Port: 3306                  │
            │    User: root                  │
            └────────────────────────────────┘
```

---

## Fluxo de Requisição HTTP

```
1. CLIENT (Browser/cURL/Postman)
   │
   └─> GET /attacks
       │
       ▼
2. CAMADA 1 (main.py)
   │
   • Route Handler: list_attacks()
   • Validação automática de Query/Body (Pydantic)
   • Injeção de dependência: db: Session = Depends(get_db)
   │
   └─> CALL services.list_attack_types(db)
       │
       ▼
3. CAMADA 2 (services.py)
   │
   • Business Logic
   • Query building: db.query(AttackType).all()
   │
   └─> CALL db.query() (SQLAlchemy)
       │
       ▼
4. CAMADA 3 (models.py + database.py)
   │
   • SQLAlchemy ORM
   • Converte Python objects → SQL queries
   • Session management
   │
   └─> EXECUTE SQL QUERY
       │
       ▼
5. CAMADA 4 (MySQL Database)
   │
   • SELECT * FROM Attack_Types
   │
   └─> RETURN RESULT SET
       │
       ▼
6. SQLAlchemy
   │
   • Converte SQL resultados → Python objects
   │
       │
       ▼
7. CAMADA 2 (services.py)
   │
   • Retorna lista de AttackType objects
   │
       │
       ▼
8. CAMADA 1 (main.py)
   │
   • Serializa com Pydantic: List[AttackTypeOut]
   • Converte para JSON
   • Adiciona HTTP headers
   │
       │
       ▼
9. CLIENT
   │
   └─> HTTP 200 OK
       Content-Type: application/json
       Body: [
         {"id": 1, "type": "Phishing"},
         {"id": 2, "type": "Ransomware"},
         ...
       ]
```

---

## Exemplo: Criar um Novo Ataque

```
POST /attacks
Content-Type: application/json
Body: {"type": "Zero-Day"}

CAMADA 1 (main.py):
├─ Route: create_attack(payload: AttackTypeIn)
├─ Validação Pydantic:
│  ├─ type: str ✓
│  ├─ min_length: 1 ✓
│  ├─ max_length: 50 ✓
│
└─ services.create_attack_type(db, payload)

CAMADA 2 (services.py):
├─ db_attack = AttackType(type=payload.type)
├─ db.add(db_attack)
├─ db.commit()
└─ db.refresh(db_attack)

CAMADA 3/4 (SQLAlchemy + MySQL):
├─ INSERT INTO Attack_Types (Type) VALUES ("Zero-Day")
├─ COMMIT transaction
└─ SELECT * FROM Attack_Types WHERE Id = LAST_INSERT_ID()

RETORNO CAMADA 1:
└─ HTTP 201 CREATED
   Content-Type: application/json
   Body: {"id": 7, "type": "Zero-Day"}
```

---

## Padrões de Design Utilizados

### 1. **MVC (Model-View-Controller)**
   - **Model**: `models.py` (SQLAlchemy models)
   - **View**: `main.py` (HTTP routes/responses)
   - **Controller**: `services.py` (business logic)

### 2. **Service Layer Pattern**
   - Separação entre rotas e lógica de negócios
   - Reutilização de código
   - Testes mais fáceis

### 3. **Dependency Injection**
   - `Depends(get_db)` para injetar a sessão do banco
   - FastAPI gerencia o ciclo de vida automático

### 4. **Schema Validation (Pydantic)**
   - Separação de modelos (DB) e schemas (API)
   - Validação automática de entrada
   - Documentação automática

### 5. **CRUD Factory**
   - Padrão repetido para cada entidade
   - list, get, create, update, delete, stats

---

## Separação de Responsabilidades

| Camada | Responsabilidade | Exemplo |
|--------|------------------|---------|
| **1: Apresentação** | HTTP, rotas, validação de entrada | `@app.get("/attacks")` |
| **2: Negócios** | Lógica, regras, filtros | `list_attack_types(db)` |
| **3: Persistência** | Acesso ao BD, mapeamento | `AttackType` class |
| **4: BD** | Armazenamento de dados | `Attack_Types` table |

---

## Tecnologias por Camada

| Camada | Tecnologias |
|--------|------------|
| **1** | FastAPI, Pydantic, Uvicorn |
| **2** | Python, Lógica pura |
| **3** | SQLAlchemy, ORM |
| **4** | MySQL, SQL |

---

Este design permite:
✅ **Escalabilidade** - Fácil adicionar novos serviços
✅ **Manutenibilidade** - Código organizado e claro
✅ **Testabilidade** - Cada camada pode ser testada isoladamente
✅ **Flexibilidade** - Trocar implementações sem afetar outras camadas
✅ **Reusabilidade** - Lógica pode ser reutilizada

