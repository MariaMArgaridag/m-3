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

from fastapi import FastAPI, HTTPException, Query, status, Depends #cria a app/http e permite que sejam enviados os erros
from pydantic import BaseModel, Field #metodo de criação de modelos de validação
from typing import Optional, List, Dict, Any  # o campo valor pode ser opcional ou uma lista
from sqlalchemy.orm import Session
from database import get_db, engine, Base
import models
import services
from schemas import (
    AttackTypeIn, AttackTypeOut,
    DefenseIn, DefenseOut,
    VulnerabilityIn, VulnerabilityOut,
    IncidentIn, IncidentOut
)

# ==========================================================
# CAMADA 1 (APRESENTAÇÃO)
# - Define rotas/endpoints
# - Valida inputs (Pydantic)
# - Define respostas HTTP
# ==========================================================

app = FastAPI(
    title="Cybersecurity Threats API",
    version="1.0.0",
    description="API REST com 4 camadas: Apresentação, Negócios, Persistência e Base de Dados"
)

# Criar tabelas no banco de dados ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

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
def list_defenses(db: Session = Depends(get_db)):
    return services.list_defense_mechanisms(db)

@app.get("/defenses/{defense_id}", response_model=DefenseOut, tags=["Defesas"])
def get_defense(defense_id: int, db: Session = Depends(get_db)):
    if defense_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid defense id")
    defense = services.get_defense_mechanism(db, defense_id)
    if not defense:
        raise HTTPException(status_code=404, detail="Defense not found")
    return defense

@app.post("/defenses", response_model=DefenseOut, status_code=status.HTTP_201_CREATED, tags=["Defesas"])
def create_defense(payload: DefenseIn, db: Session = Depends(get_db)):
    return services.create_defense_mechanism(db, payload)

@app.put("/defenses/{defense_id}", response_model=DefenseOut, tags=["Defesas"])
def update_defense(defense_id: int, payload: DefenseIn, db: Session = Depends(get_db)):
    if defense_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid defense id")
    defense = services.update_defense_mechanism(db, defense_id, payload)
    if not defense:
        raise HTTPException(status_code=404, detail="Defense not found")
    return defense

@app.delete("/defenses/{defense_id}", tags=["Defesas"])
def delete_defense(defense_id: int, db: Session = Depends(get_db)):
    if defense_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid defense id")
    deleted = services.delete_defense_mechanism(db, defense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Defense not found")
    return {"detail": "Defense deleted successfully"}

@app.get("/defenses/stats/all", tags=["Defesas"])
def defenses_stats(db: Session = Depends(get_db)):
    return services.defense_mechanisms_stats(db)


# ==========================================================
# SERVIÇO: ATAQUES (Camada 2: "Ataques")
# CRUD (5) + stats (1) = 6
# ==========================================================
@app.get("/attacks", response_model=List[AttackTypeOut], tags=["Ataques"])
def list_attacks(db: Session = Depends(get_db)):
    return services.list_attack_types(db)

@app.get("/attacks/{attack_id}", response_model=AttackTypeOut, tags=["Ataques"])
def get_attack(attack_id: int, db: Session = Depends(get_db)):
    if attack_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid attack id")
    attack = services.get_attack_type(db, attack_id)
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    return attack

@app.post("/attacks", response_model=AttackTypeOut, status_code=status.HTTP_201_CREATED, tags=["Ataques"])
def create_attack(payload: AttackTypeIn, db: Session = Depends(get_db)):
    return services.create_attack_type(db, payload)

@app.put("/attacks/{attack_id}", response_model=AttackTypeOut, tags=["Ataques"])
def update_attack(attack_id: int, payload: AttackTypeIn, db: Session = Depends(get_db)):
    if attack_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid attack id")
    attack = services.update_attack_type(db, attack_id, payload)
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    return attack

@app.delete("/attacks/{attack_id}", tags=["Ataques"])
def delete_attack(attack_id: int, db: Session = Depends(get_db)):
    if attack_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid attack id")
    deleted = services.delete_attack_type(db, attack_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Attack not found")
    return {"detail": "Attack deleted successfully"}

@app.get("/attacks/stats/all", tags=["Ataques"])
def attacks_stats(db: Session = Depends(get_db)):
    return services.attack_types_stats(db)


# ==========================================================
# SERVIÇO: VULNERABILIDADES (Camada 2: "Vulnerabilidades")
# CRUD (5) + stats (1) = 6
# ==========================================================
@app.get("/vulnerabilities", response_model=List[VulnerabilityOut], tags=["Vulnerabilidades"])
def list_vulnerabilities(db: Session = Depends(get_db)):
    return services.list_vulnerabilities(db)

@app.get("/vulnerabilities/{vuln_id}", response_model=VulnerabilityOut, tags=["Vulnerabilidades"])
def get_vulnerability(vuln_id: int, db: Session = Depends(get_db)):
    if vuln_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid vulnerability id")
    vuln = services.get_vulnerability(db, vuln_id)
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln

@app.post("/vulnerabilities", response_model=VulnerabilityOut, status_code=status.HTTP_201_CREATED, tags=["Vulnerabilidades"])
def create_vulnerability(payload: VulnerabilityIn, db: Session = Depends(get_db)):
    return services.create_vulnerability(db, payload)

@app.put("/vulnerabilities/{vuln_id}", response_model=VulnerabilityOut, tags=["Vulnerabilidades"])
def update_vulnerability(vuln_id: int, payload: VulnerabilityIn, db: Session = Depends(get_db)):
    if vuln_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid vulnerability id")
    vuln = services.update_vulnerability(db, vuln_id, payload)
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln

@app.delete("/vulnerabilities/{vuln_id}", tags=["Vulnerabilidades"])
def delete_vulnerability(vuln_id: int, db: Session = Depends(get_db)):
    if vuln_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid vulnerability id")
    deleted = services.delete_vulnerability(db, vuln_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return {"detail": "Vulnerability deleted successfully"}

@app.get("/vulnerabilities/stats/all", tags=["Vulnerabilidades"])
def vulnerabilities_stats(db: Session = Depends(get_db)):
    return services.vulnerabilities_stats(db)


# ==========================================================
# SERVIÇO: INCIDENTES (Camada 2: "Incidentes")
# CRUD (5) + stats (1) = 6
# ==========================================================
@app.get("/incidents", response_model=List[IncidentOut], tags=["Incidentes"])
def list_incidents(
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    country: Optional[str] = Query(None, description="Filtrar por país"),
    db: Session = Depends(get_db)
):
    return services.list_incidents(db, year, country)

@app.get("/incidents/{incident_id}", response_model=IncidentOut, tags=["Incidentes"])
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    if incident_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid incident id")
    incident = services.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@app.post("/incidents", response_model=IncidentOut, status_code=status.HTTP_201_CREATED, tags=["Incidentes"])
def create_incident(payload: IncidentIn, db: Session = Depends(get_db)):
    return services.create_incident(db, payload)

@app.put("/incidents/{incident_id}", response_model=IncidentOut, tags=["Incidentes"])
def update_incident(incident_id: int, payload: IncidentIn, db: Session = Depends(get_db)):
    if incident_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid incident id")
    incident = services.update_incident(db, incident_id, payload)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@app.delete("/incidents/{incident_id}", tags=["Incidentes"])
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    if incident_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid incident id")
    deleted = services.delete_incident(db, incident_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"detail": "Incident deleted successfully"}

@app.get("/incidents/stats/all", tags=["Incidentes"])
def incidents_stats(db: Session = Depends(get_db)):
    return services.incidents_stats(db)
