from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric
from database import Base

# ==================== CAMADA 3: PERSISTÊNCIA (MODELOS ORM) ====================
# Mapeia tabelas do banco de dados para classes Python

class AttackType(Base):
    """Modelo para tabela attack_types"""
    __tablename__ = "attack_types"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column('name', String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<AttackType(id={self.id}, type={self.type})>"


class DefenseMechanism(Base):
    """Modelo para tabela defense_mechanisms"""
    __tablename__ = "defense_mechanisms"
    
    id = Column(Integer, primary_key=True, index=True)
    mechanism = Column('name', String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<DefenseMechanism(id={self.id}, mechanism={self.mechanism})>"


class SecurityVulnerability(Base):
    """Modelo para tabela security_vulnerabilities"""
    __tablename__ = "security_vulnerabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    vulnerability = Column('name', String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<SecurityVulnerability(id={self.id}, vulnerability={self.vulnerability})>"


class TargetIndustry(Base):
    """Modelo para tabela target_industries"""
    __tablename__ = "target_industries"
    
    id = Column(Integer, primary_key=True, index=True)
    industry = Column('name', String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<TargetIndustry(id={self.id}, industry={self.industry})>"


class AttackSource(Base):
    """Modelo para tabela attack_sources"""
    __tablename__ = "attack_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column('name', String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<AttackSource(id={self.id}, source={self.source})>"


class GlobalCyberThreat(Base):
    """Modelo para tabela global_cyber_threats"""
    __tablename__ = "global_cyber_threats"
    
    id = Column('Id', Integer, primary_key=True, index=True)
    country = Column('Country', String(50), nullable=True)
    year = Column('Year', Integer, nullable=True)
    attack_type = Column('Attack Type', Integer, ForeignKey('attack_types.id'), nullable=True)
    target_industry = Column('Target Industry', Integer, ForeignKey('target_industries.id'), nullable=True)
    financial_loss_million = Column('Financial Loss (in Million $)', Numeric(10, 2), nullable=True)
    affected_users = Column('Number of Affected Users', Integer, nullable=True)
    attack_source = Column('Attack Source', Integer, ForeignKey('attack_sources.id'), nullable=True)
    security_vulnerability_type = Column('Security Vulnerability Type', Integer, ForeignKey('security_vulnerabilities.id'), nullable=True)
    defense_mechanism_used = Column('Defense Mechanism Used', Integer, ForeignKey('defense_mechanisms.id'), nullable=True)
    incident_resolution_time_hours = Column('Incident Resolution Time (in Hours)', Integer, nullable=True)
    
    def __repr__(self):
        return f"<GlobalCyberThreat(id={self.id}, country={self.country}, year={self.year})>"