# ==========================================================
# CAMADA 2 (NEGÓCIOS/SERVIÇOS)
# - Lógica de negócios
# - Acesso à base de dados (Camada 3)
# - Validações específicas do domínio
# ==========================================================

from sqlalchemy.orm import Session
from sqlalchemy import func
from models import (
    AttackType,
    DefenseMechanism,
    SecurityVulnerability,
    TargetIndustry,
    GlobalCyberThreat
)
from schemas import (
    AttackTypeIn, AttackTypeOut,
    DefenseIn, DefenseOut,
    VulnerabilityIn, VulnerabilityOut,
    IncidentIn, IncidentOut
)


# ==========================================================
# SERVIÇO: ATTACK TYPES (Ataques)
# ==========================================================

def list_attack_types(db: Session):
    """Listar todos os tipos de ataque"""
    return db.query(AttackType).all()


def get_attack_type(db: Session, attack_id: int):
    """Obter um tipo de ataque por ID"""
    return db.query(AttackType).filter(AttackType.id == attack_id).first()


def create_attack_type(db: Session, payload: AttackTypeIn):
    """Criar novo tipo de ataque"""
    db_attack = AttackType(type=payload.type)
    db.add(db_attack)
    db.commit()
    db.refresh(db_attack)
    return db_attack


def update_attack_type(db: Session, attack_id: int, payload: AttackTypeIn):
    """Atualizar tipo de ataque"""
    db_attack = db.query(AttackType).filter(AttackType.id == attack_id).first()
    if not db_attack:
        return None
    db_attack.type = payload.type
    db.commit()
    db.refresh(db_attack)
    return db_attack


def delete_attack_type(db: Session, attack_id: int):
    """Deletar tipo de ataque"""
    db_attack = db.query(AttackType).filter(AttackType.id == attack_id).first()
    if not db_attack:
        return False
    db.delete(db_attack)
    db.commit()
    return True


def attack_types_stats(db: Session):
    """Estatísticas de tipos de ataque"""
    total = db.query(func.count(AttackType.id)).scalar()
    return {
        "total_attack_types": total,
        "attack_types": list_attack_types(db)
    }


# ==========================================================
# SERVIÇO: DEFENSE MECHANISMS (Defesas)
# ==========================================================

def list_defense_mechanisms(db: Session):
    """Listar todos os mecanismos de defesa"""
    return db.query(DefenseMechanism).all()


def get_defense_mechanism(db: Session, defense_id: int):
    """Obter um mecanismo de defesa por ID"""
    return db.query(DefenseMechanism).filter(DefenseMechanism.id == defense_id).first()


def create_defense_mechanism(db: Session, payload: DefenseIn):
    """Criar novo mecanismo de defesa"""
    db_defense = DefenseMechanism(mechanism=payload.mechanism)
    db.add(db_defense)
    db.commit()
    db.refresh(db_defense)
    return db_defense


def update_defense_mechanism(db: Session, defense_id: int, payload: DefenseIn):
    """Atualizar mecanismo de defesa"""
    db_defense = db.query(DefenseMechanism).filter(DefenseMechanism.id == defense_id).first()
    if not db_defense:
        return None
    db_defense.mechanism = payload.mechanism
    db.commit()
    db.refresh(db_defense)
    return db_defense


def delete_defense_mechanism(db: Session, defense_id: int):
    """Deletar mecanismo de defesa"""
    db_defense = db.query(DefenseMechanism).filter(DefenseMechanism.id == defense_id).first()
    if not db_defense:
        return False
    db.delete(db_defense)
    db.commit()
    return True


def defense_mechanisms_stats(db: Session):
    """Estatísticas de mecanismos de defesa"""
    total = db.query(func.count(DefenseMechanism.id)).scalar()
    return {
        "total_defense_mechanisms": total,
        "defense_mechanisms": list_defense_mechanisms(db)
    }


# ==========================================================
# SERVIÇO: SECURITY VULNERABILITIES (Vulnerabilidades)
# ==========================================================

def list_vulnerabilities(db: Session):
    """Listar todas as vulnerabilidades"""
    return db.query(SecurityVulnerability).all()


def get_vulnerability(db: Session, vuln_id: int):
    """Obter uma vulnerabilidade por ID"""
    return db.query(SecurityVulnerability).filter(SecurityVulnerability.id == vuln_id).first()


def create_vulnerability(db: Session, payload: VulnerabilityIn):
    """Criar nova vulnerabilidade"""
    db_vuln = SecurityVulnerability(vulnerability=payload.vulnerability)
    db.add(db_vuln)
    db.commit()
    db.refresh(db_vuln)
    return db_vuln


def update_vulnerability(db: Session, vuln_id: int, payload: VulnerabilityIn):
    """Atualizar vulnerabilidade"""
    db_vuln = db.query(SecurityVulnerability).filter(SecurityVulnerability.id == vuln_id).first()
    if not db_vuln:
        return None
    db_vuln.vulnerability = payload.vulnerability
    db.commit()
    db.refresh(db_vuln)
    return db_vuln


def delete_vulnerability(db: Session, vuln_id: int):
    """Deletar vulnerabilidade"""
    db_vuln = db.query(SecurityVulnerability).filter(SecurityVulnerability.id == vuln_id).first()
    if not db_vuln:
        return False
    db.delete(db_vuln)
    db.commit()
    return True


def vulnerabilities_stats(db: Session):
    """Estatísticas de vulnerabilidades"""
    total = db.query(func.count(SecurityVulnerability.id)).scalar()
    return {
        "total_vulnerabilities": total,
        "vulnerabilities": list_vulnerabilities(db)
    }


# ==========================================================
# SERVIÇO: TARGET INDUSTRIES (Indústrias Alvo)
# ==========================================================

def list_industries(db: Session):
    """Listar todas as indústrias alvo"""
    return db.query(TargetIndustry).all()


def get_industry(db: Session, industry_id: int):
    """Obter uma indústria por ID"""
    return db.query(TargetIndustry).filter(TargetIndustry.id == industry_id).first()


def create_industry(db: Session, industry_name: str):
    """Criar nova indústria"""
    db_industry = TargetIndustry(industry=industry_name)
    db.add(db_industry)
    db.commit()
    db.refresh(db_industry)
    return db_industry


def update_industry(db: Session, industry_id: int, industry_name: str):
    """Atualizar indústria"""
    db_industry = db.query(TargetIndustry).filter(TargetIndustry.id == industry_id).first()
    if not db_industry:
        return None
    db_industry.industry = industry_name
    db.commit()
    db.refresh(db_industry)
    return db_industry


def delete_industry(db: Session, industry_id: int):
    """Deletar indústria"""
    db_industry = db.query(TargetIndustry).filter(TargetIndustry.id == industry_id).first()
    if not db_industry:
        return False
    db.delete(db_industry)
    db.commit()
    return True


def industries_stats(db: Session):
    """Estatísticas de indústrias"""
    total = db.query(func.count(TargetIndustry.id)).scalar()
    return {
        "total_industries": total,
        "industries": list_industries(db)
    }


# ==========================================================
# SERVIÇO: INCIDENTS (Incidentes)
# ==========================================================

def list_incidents(db: Session, year: int = None, country: str = None):
    """Listar incidentes com filtros opcionais"""
    query = db.query(GlobalCyberThreat)
    
    if year:
        query = query.filter(GlobalCyberThreat.year == year)
    if country:
        query = query.filter(GlobalCyberThreat.country == country)
    
    return query.all()


def get_incident(db: Session, incident_id: int):
    """Obter um incidente por ID"""
    return db.query(GlobalCyberThreat).filter(GlobalCyberThreat.id == incident_id).first()


def create_incident(db: Session, payload: IncidentIn):
    """Criar novo incidente"""
    db_incident = GlobalCyberThreat(
        country=payload.country,
        year=payload.year,
        attack_type=payload.attack_type,
        target_industry=payload.target_industry,
        financial_loss_million=payload.financial_loss_million,
        affected_users=payload.affected_users,
        attack_source=payload.attack_source,
        security_vulnerability_type=payload.security_vulnerability_type,
        defense_mechanism_used=payload.defense_mechanism_used,
        incident_resolution_time_hours=payload.incident_resolution_time_hours
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def update_incident(db: Session, incident_id: int, payload: IncidentIn):
    """Atualizar incidente"""
    db_incident = db.query(GlobalCyberThreat).filter(GlobalCyberThreat.id == incident_id).first()
    if not db_incident:
        return None
    
    # Atualizar apenas campos fornecidos (não None)
    if payload.country is not None:
        db_incident.country = payload.country
    if payload.year is not None:
        db_incident.year = payload.year
    if payload.attack_type is not None:
        db_incident.attack_type = payload.attack_type
    if payload.target_industry is not None:
        db_incident.target_industry = payload.target_industry
    if payload.financial_loss_million is not None:
        db_incident.financial_loss_million = payload.financial_loss_million
    if payload.affected_users is not None:
        db_incident.affected_users = payload.affected_users
    if payload.attack_source is not None:
        db_incident.attack_source = payload.attack_source
    if payload.security_vulnerability_type is not None:
        db_incident.security_vulnerability_type = payload.security_vulnerability_type
    if payload.defense_mechanism_used is not None:
        db_incident.defense_mechanism_used = payload.defense_mechanism_used
    if payload.incident_resolution_time_hours is not None:
        db_incident.incident_resolution_time_hours = payload.incident_resolution_time_hours
    
    db.commit()
    db.refresh(db_incident)
    return db_incident


def delete_incident(db: Session, incident_id: int):
    """Deletar incidente"""
    db_incident = db.query(GlobalCyberThreat).filter(GlobalCyberThreat.id == incident_id).first()
    if not db_incident:
        return False
    db.delete(db_incident)
    db.commit()
    return True


def incidents_stats(db: Session):
    """Estatísticas de incidentes"""
    total_incidents = db.query(func.count(GlobalCyberThreat.id)).scalar()
    total_financial_loss = db.query(func.sum(GlobalCyberThreat.financial_loss_million)).scalar()
    total_affected_users = db.query(func.sum(GlobalCyberThreat.affected_users)).scalar()
    avg_resolution_time = db.query(func.avg(GlobalCyberThreat.incident_resolution_time_hours)).scalar()
    
    return {
        "total_incidents": total_incidents,
        "total_financial_loss_million": float(total_financial_loss) if total_financial_loss else 0,
        "total_affected_users": total_affected_users if total_affected_users else 0,
        "average_resolution_time_hours": float(avg_resolution_time) if avg_resolution_time else 0
    }
