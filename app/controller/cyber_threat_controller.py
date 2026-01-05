from flask import Blueprint, request, jsonify
from service.cyber_threat_service import CyberThreatService
from repository.cyber_threat_repository import CyberThreatRepository
from database import db

cyber_threat_bp = Blueprint("cyber_threats", __name__, url_prefix="/cyber_threats")
service = CyberThreatService(CyberThreatRepository(db))

@cyber_threat_bp.post("/")
def create_cyber_threat():
    """
    Criar nova ameaça cibernética
    ---
    tags:
      - CyberThreats
    summary: "Create Cyber Threat"
    description: "Registra um novo incidente/ameaça de cibersegurança"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - country
            - year
            - attack_type
            - target_industry
            - financial_loss
            - affected_users
            - security_vulnerability
            - defense_mechanism
            - resolution_time
          properties:
            country:
              type: string
              example: "Brasil"
            year:
              type: integer
              example: 2024
            attack_type:
              type: integer
              example: 1
            target_industry:
              type: integer
              example: 2
            financial_loss:
              type: number
              example: 1000000.00
            affected_users:
              type: integer
              example: 5000
            security_vulnerability:
              type: integer
              example: 1
            defense_mechanism:
              type: integer
              example: 2
            resolution_time:
              type: integer
              example: 48
    responses:
      201:
        description: Ameaça criada com sucesso
        schema:
          type: object
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.json or {}

    country = data.get("country")
    year = data.get("year")
    attack_type = data.get("attack_type")
    target_industry = data.get("target_industry")
    financial_loss = data.get("financial_loss")
    affected_users = data.get("affected_users")
    security_vulnerability = data.get("security_vulnerability")
    defense_mechanism = data.get("defense_mechanism")
    resolution_time = data.get("resolution_time")

    if not country or not isinstance(country, str):
        return {"error": "Invalid country"}, 400
    if year is None or not isinstance(year, int):
        return {"error": "Invalid year"}, 400
    if attack_type is None or not isinstance(attack_type, int):
        return {"error": "Invalid attack_type"}, 400
    if target_industry is None or not isinstance(target_industry, int):
        return {"error": "Invalid target_industry"}, 400
    if financial_loss is None or not isinstance(financial_loss, (int, float)):
        return {"error": "Invalid financial_loss"}, 400
    if affected_users is None or not isinstance(affected_users, int):
        return {"error": "Invalid affected_users"}, 400
    if security_vulnerability is None or not isinstance(security_vulnerability, int):
        return {"error": "Invalid security_vulnerability"}, 400
    if defense_mechanism is None or not isinstance(defense_mechanism, int):
        return {"error": "Invalid defense_mechanism"}, 400
    if resolution_time is None or not isinstance(resolution_time, int):
        return {"error": "Invalid resolution_time"}, 400

    result = service.create(country, year, attack_type, target_industry, financial_loss, affected_users, security_vulnerability, defense_mechanism, resolution_time)

    if result is None:
        return {"error": "Invalid parameters"}

    return jsonify(result), 201

@cyber_threat_bp.get("/")
def list_cyber_threats():
    """
    Listar todas as ameaças cibernéticas
    ---
    tags:
      - CyberThreats
    summary: "List All Cyber Threats"
    description: "Retorna uma lista de todos os incidentes de cibersegurança"
    responses:
      200:
        description: Lista de ameaças cibernéticas
        schema:
          type: array
          items:
            type: object
    """
    return jsonify(service.list())

@cyber_threat_bp.get("/<int:id>")
def get_by_id_cyber_threat(id):
    """
    Obter ameaça cibernética por ID
    ---
    tags:
      - CyberThreats
    summary: "Read Cyber Threat"
    description: "Retorna um incidente específico pelo seu ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único da ameaça
    responses:
      200:
        description: Ameaça encontrada
        schema:
          type: object
      404:
        description: Ameaça não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    result = service.get_by_id(id)

    if result is None:
        return {"error": "Not found"}, 404

    return result

@cyber_threat_bp.put("/<int:id>")
def update_cyber_threat(id):
    """
    Atualizar ameaça cibernética
    ---
    tags:
      - CyberThreats
    summary: "Update Cyber Threat"
    description: "Atualiza as informações de um incidente existente"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único da ameaça
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            country:
              type: string
            year:
              type: integer
            attack_type:
              type: integer
            target_industry:
              type: integer
            financial_loss:
              type: number
            affected_users:
              type: integer
            security_vulnerability:
              type: integer
            defense_mechanism:
              type: integer
            resolution_time:
              type: integer
    responses:
      200:
        description: Ameaça atualizada com sucesso
        schema:
          type: object
      404:
        description: Ameaça não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.json or {}

    result = service.update(
        id=id,
        country=data.get("country"),
        year=data.get("year"),
        attack_type=data.get("attack_type"),
        target_industry=data.get("target_industry"),
        financial_loss=data.get("financial_loss"),
        affected_users=data.get("affected_users"),
        security_vulnerability=data.get("security_vulnerability"),
        defense_mechanism=data.get("defense_mechanism"),
        resolution_time=data.get("resolution_time"),
    )

    if result is None:
        return {"error": "Not found"}, 404

    return jsonify(result)

@cyber_threat_bp.delete("/<int:id>")
def delete_cyber_threat(id):
    """
    Deletar ameaça cibernética
    ---
    tags:
      - CyberThreats
    summary: "Delete Cyber Threat"
    description: "Remove um incidente do sistema"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único da ameaça
    responses:
      204:
        description: Ameaça deletada com sucesso
      404:
        description: Ameaça não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    result = service.delete(id)

    if result is False:
        return {"error": "Not found"}, 404

    return "", 204

@cyber_threat_bp.get("/attack_types")
def attack_type_percentage():
    """
    Análise de ameaças por tipo de ataque
    ---
    tags:
      - CyberThreats
    summary: "Threat Analysis by Attack Type"
    description: "Retorna estatísticas das ameaças agrupadas por tipo de ataque"
    responses:
      200:
        description: Estatísticas por tipo
        schema:
          type: object
    """
    return service.attack_type_percentage()

@cyber_threat_bp.get("/defense_mechanism")
def defense_mechanism_percentage():
    """
    Análise de ameaças por mecanismo de defesa
    ---
    tags:
      - CyberThreats
    summary: "Threat Analysis by Defense Mechanism"
    description: "Retorna estatísticas das ameaças agrupadas por mecanismo de defesa"
    responses:
      200:
        description: Estatísticas por defesa
        schema:
          type: object
    """
    return service.defense_mechanism_percentage()

@cyber_threat_bp.get("/security_vulnerability")
def security_vulnerability_percentage():
    """
    Análise de ameaças por vulnerabilidade
    ---
    tags:
      - CyberThreats
    summary: "Threat Analysis by Vulnerability"
    description: "Retorna estatísticas das ameaças agrupadas por vulnerabilidade"
    responses:
      200:
        description: Estatísticas por vulnerabilidade
        schema:
          type: object
    """
    return service.security_vulnerability_percentage()

@cyber_threat_bp.get("/target_industry")
def target_industry_percentage():
    """
    Análise de ameaças por indústria alvo
    ---
    tags:
      - CyberThreats
    summary: "Threat Analysis by Target Industry"
    description: "Retorna estatísticas das ameaças agrupadas por indústria alvo"
    responses:
      200:
        description: Estatísticas por indústria
        schema:
          type: object
    """
    return service.target_industry_percentage()