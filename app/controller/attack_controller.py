from flask import Blueprint, request, jsonify
from service.attack_service import AttackService
from repository.attack_repository import AttackRepository
from database import db

attack_bp = Blueprint("attacks", __name__, url_prefix="/attacks")
service = AttackService(AttackRepository(db))

@attack_bp.post("/")
def create_attack():
    """
    Criar novo ataque
    ---
    tags:
      - Attacks
    summary: "Create Attack"
    description: "Registra um novo ataque cibernético no sistema"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - attack_type
            - attack_source
            - target_industry
            - country
            - year
            - financial_loss
            - affected_users
          properties:
            attack_type:
              type: integer
              description: ID do tipo de ataque
              example: 1
            attack_source:
              type: integer
              description: ID da fonte de ataque
              example: 2
            target_industry:
              type: integer
              description: ID da indústria alvo
              example: 3
            country:
              type: string
              description: País onde o ataque ocorreu
              example: "Brasil"
            year:
              type: integer
              description: Ano do ataque
              example: 2024
            financial_loss:
              type: number
              description: Perda financeira em USD
              example: 500000.50
            affected_users:
              type: integer
              description: Número de usuários afetados
              example: 1000
    responses:
      201:
        description: Ataque criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: string
              example: "550e8400-e29b-41d4-a716-446655440001"
            attack_type:
              type: integer
            attack_source:
              type: integer
            target_industry:
              type: integer
            country:
              type: string
            year:
              type: integer
            financial_loss:
              type: number
            affected_users:
              type: integer
      400:
        description: Dados inválidos ou incompletos
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.json or {}

    attack_type = data.get("attack_type")
    attack_source = data.get("attack_source")
    target_industry = data.get("target_industry")
    country = data.get("country")
    year = data.get("year")
    financial_loss = data.get("financial_loss")
    affected_users = data.get("affected_users")

    if attack_type is None or not isinstance(attack_type, int):
        return {"error": "Invalid attack_type"}, 400
    if attack_source is None or not isinstance(attack_source, int):
        return {"error": "Invalid attack_source"}, 400
    if target_industry is None or not isinstance(target_industry, int):
        return {"error": "Invalid target_industry"}, 400
    if not country or not isinstance(country, str):
        return {"error": "Invalid country"}, 400
    if year is None or not isinstance(year, int):
        return {"error": "Invalid year"}, 400
    if financial_loss is None or not isinstance(financial_loss, (int, float)):
        return {"error": "Invalid financial_loss"}, 400
    if affected_users is None or not isinstance(affected_users, int):
        return {"error": "Invalid affected_users"}, 400

    result = service.create(attack_type, attack_source, target_industry, 
                           country, year, financial_loss, affected_users)

    if result is None:
        return {"error": "Invalid parameters"}, 400

    return jsonify(result), 201

@attack_bp.get("/")
def list_attacks():
    """
    Listar todos os ataques
    ---
    tags:
      - Attacks
    summary: "List All Attacks"
    description: "Retorna uma lista de todos os ataques registrados"
    responses:
      200:
        description: Lista de ataques
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "550e8400-e29b-41d4-a716-446655440001"
              attack_type:
                type: integer
              attack_source:
                type: integer
              target_industry:
                type: integer
              country:
                type: string
              year:
                type: integer
              financial_loss:
                type: number
              affected_users:
                type: integer
    """
    return jsonify(service.list())

@attack_bp.get("/<string:external_id>")
def get_by_id_attack(external_id):
    """
    Obter ataque por ID
    ---
    tags:
      - Attacks
    summary: "Read Attack"
    description: "Retorna um ataque específico pelo seu ID"
    parameters:
      - in: path
        name: external_id
        type: string
        required: true
        description: ID único do ataque
        example: "550e8400-e29b-41d4-a716-446655440001"
    responses:
      200:
        description: Ataque encontrado
        schema:
          type: object
      404:
        description: Ataque não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    result = service.get_by_id(external_id)

    if result is None:
        return {"error": "Not found"}, 404

    return result

@attack_bp.put("/<string:external_id>")
def update_attack(external_id):
    """
    Atualizar ataque
    ---
    tags:
      - Attacks
    summary: "Update Attack"
    description: "Atualiza as informações de um ataque existente"
    parameters:
      - in: path
        name: external_id
        type: string
        required: true
        description: ID único do ataque
        example: "550e8400-e29b-41d4-a716-446655440001"
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            attack_type:
              type: integer
            attack_source:
              type: integer
            target_industry:
              type: integer
            country:
              type: string
            year:
              type: integer
            financial_loss:
              type: number
            affected_users:
              type: integer
    responses:
      200:
        description: Ataque atualizado com sucesso
        schema:
          type: object
      404:
        description: Ataque não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    data = request.json or {}

    result = service.update(
        external_id=external_id,
        attack_type=data.get("attack_type"),
        attack_source=data.get("attack_source"),
        target_industry=data.get("target_industry"),
        country=data.get("country"),
        year=data.get("year"),
        financial_loss=data.get("financial_loss"),
        affected_users=data.get("affected_users")
    )

    if result is None:
        return {"error": "Not found"}, 404

    return jsonify(result)

@attack_bp.delete("/<string:external_id>")
def delete_attack(external_id):
    """
    Deletar ataque
    ---
    tags:
      - Attacks
    summary: "Delete Attack"
    description: "Remove um ataque do sistema"
    parameters:
      - in: path
        name: external_id
        type: string
        required: true
        description: ID único do ataque
        example: "550e8400-e29b-41d4-a716-446655440001"
    responses:
      204:
        description: Ataque deletado com sucesso
      404:
        description: Ataque não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    result = service.delete(external_id)

    if result is False:
        return {"error": "Not found"}, 404

    return "", 204

@attack_bp.get("/statistics")
def attack_statistics():
    """
    Obter estatísticas de ataques
    ---
    tags:
      - Attacks
    summary: "Get Attack Statistics"
    description: "Retorna estatísticas e análises sobre os ataques"
    responses:
      200:
        description: Estatísticas dos ataques
        schema:
          type: object
          properties:
            total:
              type: integer
            average_loss:
              type: number
            most_affected_industry:
              type: string
    """
    return jsonify(service.statistics())




