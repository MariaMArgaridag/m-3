from flask import Blueprint, request, jsonify
from service.defense_mechanism_service import DefenseMechanismService
from repository.defense_mechanism_repository import DefenseMechanismRepository
from database import db

defense_mechanism_bp = Blueprint("defense_mechanisms", __name__, url_prefix="/defense_mechanisms")
service = DefenseMechanismService(DefenseMechanismRepository(db))

@defense_mechanism_bp.post("/")
def create_defense_mechanism():
    """
    Criar novo mecanismo de defesa
    ---
    tags:
      - DefenseMechanisms
    summary: "Create Defense Mechanism"
    description: "Cria um novo mecanismo de defesa no sistema"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - mechanism
          properties:
            mechanism:
              type: string
              description: Nome do mecanismo de defesa
              example: "Firewall com IA"
    responses:
      201:
        description: Mecanismo de defesa criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: string
              example: "550e8400-e29b-41d4-a716-446655440000"
            mechanism:
              type: string
              example: "Firewall com IA"
      400:
        description: Dados inválidos ou incompletos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Mechanism invalid"
    """
    data = request.json or {}

    mechanism = data.get("mechanism")

    if not mechanism or not isinstance(mechanism, str):
        return {"error": "Mechanism invalid"}, 400

    return jsonify(
        service.create(mechanism)
    ), 201

@defense_mechanism_bp.get("/")
def list_defense_mechanisms():
    """
    Listar todos os mecanismos de defesa
    ---
    tags:
      - DefenseMechanisms
    summary: "List All Defense Mechanisms"
    description: "Retorna uma lista de todos os mecanismos de defesa registrados"
    responses:
      200:
        description: Lista de mecanismos de defesa
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "550e8400-e29b-41d4-a716-446655440000"
              mechanism:
                type: string
                example: "Firewall com IA"
    """
    return jsonify(service.list())

@defense_mechanism_bp.get("/<string:external_id>")
def get_by_id_defense_mechanism(external_id):
    """
    Obter mecanismo de defesa por ID
    ---
    tags:
      - DefenseMechanisms
    summary: "Read Defense Mechanism"
    description: "Retorna um mecanismo de defesa específico pelo seu ID"
    parameters:
      - in: path
        name: external_id
        type: string
        required: true
        description: ID único do mecanismo de defesa
        example: "550e8400-e29b-41d4-a716-446655440000"
    responses:
      200:
        description: Mecanismo de defesa encontrado
        schema:
          type: object
          properties:
            id:
              type: string
              example: "550e8400-e29b-41d4-a716-446655440000"
            mechanism:
              type: string
              example: "Firewall com IA"
      404:
        description: Mecanismo de defesa não encontrado
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

@defense_mechanism_bp.put("/<string:external_id>")
def update_defense_mechanism(external_id):
    """
    Atualizar mecanismo de defesa
    ---
    tags:
      - DefenseMechanisms
    summary: "Update Defense Mechanism"
    description: "Atualiza as informações de um mecanismo de defesa existente"
    parameters:
      - in: path
        name: external_id
        type: string
        required: true
        description: ID único do mecanismo de defesa
        example: "550e8400-e29b-41d4-a716-446655440000"
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - mechanism
          properties:
            mechanism:
              type: string
              description: Novo nome do mecanismo de defesa
              example: "Firewall com Machine Learning"
    responses:
      200:
        description: Mecanismo de defesa atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: string
              example: "550e8400-e29b-41d4-a716-446655440000"
            mechanism:
              type: string
              example: "Firewall com Machine Learning"
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Mechanism invalid"
      404:
        description: Mecanismo de defesa não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
    """
    data = request.json or {}

    mechanism = data.get("mechanism")

    if not mechanism or not isinstance(mechanism, str):
        return {"error": "Mechanism invalid"}, 400
    
    result = service.update(external_id, mechanism)

    if result is None:
        return {"error": "Not found"}, 404
    
    return result

@defense_mechanism_bp.delete("/<string:external_id>")
def delete_defense_mechanism(external_id):
    """
    Deletar mecanismo de defesa
    ---
    tags:
      - DefenseMechanisms
    summary: "Delete Defense Mechanism"
    description: "Remove um mecanismo de defesa do sistema"
    parameters:
      - in: path
        name: external_id
        type: string
        required: true
        description: ID único do mecanismo de defesa
        example: "550e8400-e29b-41d4-a716-446655440000"
    responses:
      204:
        description: Mecanismo de defesa deletado com sucesso
      404:
        description: Mecanismo de defesa não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Not found"
      409:
        description: Não pode ser deletado (relacionado com outras entidades)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "It cannot be deleted"
    """
    result = service.delete(external_id)

    if result is False:
        return {"error": "Not found"}, 404

    if result == "FK":
        return {
            "error": "It cannot be deleted"
        }, 409

    return "", 204

@defense_mechanism_bp.get("/statistics")
def defense_mechanism_statistics():
    """
    Obter estatísticas de mecanismos de defesa
    ---
    tags:
      - DefenseMechanisms
    summary: "Get Defense Mechanism Statistics"
    description: "Retorna estatísticas e análises sobre os mecanismos de defesa"
    responses:
      200:
        description: Estatísticas dos mecanismos de defesa
        schema:
          type: object
          properties:
            total:
              type: integer
              example: 5
            average_efficiency:
              type: number
              example: 85.5
    """
    return jsonify(service.statistics())