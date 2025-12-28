#from fastapi import FastAPI
#from fastapi import FastAPI, HTTPException
#from pydantic import BaseModel
#from typing import List

#app = FastAPI()


#Dados da base de dados, neste caso os que iremso utilizar
#Criação deste dicionário
#db = { 
 #     "Defense Mechanisms": [], 
  #    "Target Industry": [], 
    #  "Vulnerabilities": [], 
     # "Attack Type": [] 
     # }

#Cria a rota para o fast api, usando o que se pretende /get, post, put, delete) 
#@app.get("/threats")
#def threats():      # ✅ nome decidido por ti
 #  return {"status": "ok"}

from fastapi import FastAPI, HTTPException, Query, status #cria a app/http e permite que sejam enviados os erros
from pydantic import BaseModel, Field #metodo de criação de modelos de validação
from typing import Optional, List, Dict, Any  # o campo valor pode ser opcional ou uma lista

# ==========================================================
# CAMADA 1 (APRESENTAÇÃO)
# - Define rotas/endpoints
# - Valida inputs (Pydantic)
# - Define respostas HTTP
# ==========================================================

app = FastAPI(
    title="Cybersecurity Threats API",
    version="1.0.0",
    description="Camada 1: Rotas REST + validação + OpenAPI3"
)

#Criação dos dicionários

ATTACK_TYPES = {
    1: "Phishing",
    2: "Ransomware",
    3: "Man-in-the-Middle",
    4: "DDoS",
    5: "SQL Injection",
    6: "Malware",
}

DEFENSE_MECHANISMS = {
    1: "VPN",
    2: "Firewall",
    3: "AI-based Detection",
    4: "Antivirus",
    5: "Encryption",
    8: "Zero Trust",
}

VULNERABILITIES = {
    1: "Unpatched Software",
    2: "Weak Passwords",
    3: "Social Engineering",
    4: "Zero-day",
}

INDUSTRIES = {
    1: "Education",
    2: "Retail",
    3: "IT",
    4: "Telecommunications",
    5: "Government",
    6: "Banking",
    7: "Healthcare",
}

# ==========================================================
# MODELOS (VALIDAÇÃO) dos dados que entram na API- usados no POST/PUT
# ==========================================================
#campo de mecanismo é obrigatório! em seguida limita que não pde estar vazio e o maximo são 50 caracteres
# ---- DEFESAS (Defense_Mechanisms) ----

class DefenseIn(BaseModel):
    mechanism: str = Field(..., min_length=1, max_length=50)

class DefenseOut(BaseModel):
    id: int
    mechanism: str

#cliente envia o nome do ataque
#Envia o ID e o tipo - está errado nao pode devolver o id

# ---- ATAQUES (Attack_Types) ----
class AttackTypeIn(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)

class AttackTypeOut(BaseModel):
    id: int
    type: str

# ---- VULNERABILIDADES (Security_Vulnerabilities) ----
class VulnerabilityIn(BaseModel):
    vulnerability: str = Field(..., min_length=1, max_length=50)

class VulnerabilityOut(BaseModel):
    id: int
    vulnerability: str

# ---- INCIDENTES (global_cyber_threats) ----
# A tua tabela tem campos com espaços. Em Python usamos snake_case, isto porque no sql existem espaços.
#Ira também atualizar quando o cliente nos fornecer dados de entrada, através do PUT.
class IncidentIn(BaseModel):
    country: Optional[str] = Field(None, max_length=50)
    year: Optional[int] = Field(None, ge=1900, le=2100)

    attack_type: Optional[int] = Field(None, gt=0)
    target_industry: Optional[int] = Field(None, gt=0)

    financial_loss_million: Optional[float] = Field(None, ge=0)
    affected_users: Optional[int] = Field(None, ge=0)

    attack_source: Optional[int] = Field(None, gt=0)
    security_vulnerability_type: Optional[int] = Field(None, gt=0)
    defense_mechanism_used: Optional[int] = Field(None, gt=0)

    incident_resolution_time_hours: Optional[int] = Field(None, ge=0)

class IncidentOut(BaseModel):
    id: int
    country: Optional[str] = None
    year: Optional[int] = None
    attack_type: Optional[int] = None
    target_industry: Optional[int] = None
    financial_loss_million: Optional[float] = None
    affected_users: Optional[int] = None
    attack_source: Optional[int] = None
    security_vulnerability_type: Optional[int] = None
    defense_mechanism_used: Optional[int] = None
    incident_resolution_time_hours: Optional[int] = None


# ==========================================================
# HEALTH (para testar se a API está a correr)
# ==========================================================
@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}


# ==========================================================
# SERVIÇO: DEFESAS (Camada 2: "Defesas") vai criar as routas para a defense, e posteriomente é necessário alterar após ser feita a camada 2, 
#vai ser feito em todas as varieaveis.
# CRUD (5) + stats (1) = 6
# ==========================================================
@app.get("/defenses", response_model=List[DefenseOut], tags=["Defesas"])
def list_defenses():
    # TODO (Camada 2): return services.list_defenses()
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/defenses/{defense_id}", response_model=DefenseOut, tags=["Defesas"])
def get_defense(defense_id: int):
    if defense_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid defense id")
    # TODO (Camada 2): return services.get_defense(defense_id)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.post("/defenses", response_model=DefenseOut, status_code=status.HTTP_201_CREATED, tags=["Defesas"])
def create_defense(payload: DefenseIn):
    # TODO (Camada 2): return services.create_defense(payload)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.put("/defenses/{defense_id}", response_model=DefenseOut, tags=["Defesas"])
def update_defense(defense_id: int, payload: DefenseIn):
    if defense_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid defense id")
    # TODO (Camada 2): return services.update_defense(defense_id, payload)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.delete("/defenses/{defense_id}", tags=["Defesas"])
def delete_defense(defense_id: int):
    if defense_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid defense id")
    # TODO (Camada 2): services.delete_defense(defense_id)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/defenses/stats", tags=["Defesas"])
def defenses_stats():
    # TODO (Camada 2): return services.defenses_stats()
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")


# ==========================================================
# SERVIÇO: ATAQUES (Camada 2: "Ataques")
# CRUD (5) + stats (1) = 6
# ==========================================================
@app.get("/attacks", response_model=List[AttackTypeOut], tags=["Ataques"])
def list_attacks():
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/attacks/{attack_id}", response_model=AttackTypeOut, tags=["Ataques"])
def get_attack(attack_id: int):
    if attack_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid attack id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.post("/attacks", response_model=AttackTypeOut, status_code=status.HTTP_201_CREATED, tags=["Ataques"])
def create_attack(payload: AttackTypeIn):
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.put("/attacks/{attack_id}", response_model=AttackTypeOut, tags=["Ataques"])
def update_attack(attack_id: int, payload: AttackTypeIn):
    if attack_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid attack id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.delete("/attacks/{attack_id}", tags=["Ataques"])
def delete_attack(attack_id: int):
    if attack_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid attack id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/attacks/stats", tags=["Ataques"])
def attacks_stats():
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")


# ==========================================================
# SERVIÇO: VULNERABILIDADES (Camada 2: "Vulnerabilidades")
# CRUD (5) + stats (1) = 6
# ==========================================================
@app.get("/vulnerabilities", response_model=List[VulnerabilityOut], tags=["Vulnerabilidades"])
def list_vulnerabilities():
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/vulnerabilities/{vuln_id}", response_model=VulnerabilityOut, tags=["Vulnerabilidades"])
def get_vulnerability(vuln_id: int):
    if vuln_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid vulnerability id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.post("/vulnerabilities", response_model=VulnerabilityOut, status_code=status.HTTP_201_CREATED, tags=["Vulnerabilidades"])
def create_vulnerability(payload: VulnerabilityIn):
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.put("/vulnerabilities/{vuln_id}", response_model=VulnerabilityOut, tags=["Vulnerabilidades"])
def update_vulnerability(vuln_id: int, payload: VulnerabilityIn):
    if vuln_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid vulnerability id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.delete("/vulnerabilities/{vuln_id}", tags=["Vulnerabilidades"])
def delete_vulnerability(vuln_id: int):
    if vuln_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid vulnerability id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/vulnerabilities/stats", tags=["Vulnerabilidades"])
def vulnerabilities_stats():
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")


# ==========================================================
# SERVIÇO: INCIDENTES (Camada 2: "Incidentes")
# CRUD (5) + stats (1) = 6
# ==========================================================
@app.get("/incidents", response_model=List[IncidentOut], tags=["Incidentes"])
def list_incidents(
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    country: Optional[str] = Query(None, description="Filtrar por país")
):
    # TODO (Camada 2): return services.list_incidents(year, country)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/incidents/{incident_id}", response_model=IncidentOut, tags=["Incidentes"])
def get_incident(incident_id: int):
    if incident_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid incident id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.post("/incidents", response_model=IncidentOut, status_code=status.HTTP_201_CREATED, tags=["Incidentes"])
def create_incident(payload: IncidentIn):
    # TODO (Camada 2): validar FKs + inserir
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.put("/incidents/{incident_id}", response_model=IncidentOut, tags=["Incidentes"])
def update_incident(incident_id: int, payload: IncidentIn):
    if incident_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid incident id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.delete("/incidents/{incident_id}", tags=["Incidentes"])
def delete_incident(incident_id: int):
    if incident_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid incident id")
    # TODO (Camada 2)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")

@app.get("/incidents/stats", tags=["Incidentes"])
def incidents_stats():
    # TODO (Camada 2): estatísticas (ex.: perdas totais, por ano, por tipo)
    raise HTTPException(status_code=501, detail="Implementar na Camada 2")
