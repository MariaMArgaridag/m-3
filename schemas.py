# ==========================================================
# SCHEMAS (Modelos Pydantic para validação de dados)
# Separados para evitar importação circular
# ==========================================================

from pydantic import BaseModel, Field
from typing import Optional


# ---- DEFESAS (Defense_Mechanisms) ----
class DefenseIn(BaseModel):
    mechanism: str = Field(..., min_length=1, max_length=50)


class DefenseOut(BaseModel):
    id: int
    mechanism: str
    
    class Config:
        from_attributes = True


# ---- ATAQUES (Attack_Types) ----
class AttackTypeIn(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)


class AttackTypeOut(BaseModel):
    id: int
    type: str
    
    class Config:
        from_attributes = True


# ---- VULNERABILIDADES (Security_Vulnerabilities) ----
class VulnerabilityIn(BaseModel):
    vulnerability: str = Field(..., min_length=1, max_length=50)


class VulnerabilityOut(BaseModel):
    id: int
    vulnerability: str
    
    class Config:
        from_attributes = True


# ---- INCIDENTES (global_cyber_threats) ----
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
    
    class Config:
        from_attributes = True
