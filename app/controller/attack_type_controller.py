from flask import Blueprint, request, jsonify
from service.attack_type_service import AttackTypeService
from repository.attack_type_repository import AttackTypeRepository
from database import db

attack_type_bp = Blueprint("attack_types", __name__, url_prefix="/attack_types")
service = AttackTypeService(AttackTypeRepository(db))

@attack_type_bp.post("/")
def create_attack_type():
    """
    Criar novo tipo de ataque
    ---
    tags:
      - AttackTypes
    summary: "Create Attack Type"
    description: "Registra uma nova classificação/tipo de ataque"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - type
          properties:
            type:
              type: string
              description: Nome do tipo de ataque
              example: "Ransomware"
    responses:
      201:
        description: Tipo de ataque criado com sucesso
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

    type = data.get("type")

    if not type or not isinstance(type, str):
        return {"error": "Invalid type"}, 400

    return jsonify(
        service.create(type)
    ), 201

@attack_type_bp.get("/")
def list_attack_types():
    """
    Listar todos os tipos de ataque
    ---
    tags:
      - AttackTypes
    summary: "List All Attack Types"
    description: "Retorna uma lista de todos os tipos/classificações de ataque"
    responses:
      200:
        description: Lista de tipos de ataque
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              type:
                type: string
    """
    return jsonify(service.list())

@attack_type_bp.get("/<int:id>")
def get_by_id_attack_type(id):
    """
    Obter tipo de ataque por ID
    ---
    tags:
      - AttackTypes
    summary: "Read Attack Type"
    description: "Retorna um tipo de ataque específico pelo seu ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único do tipo de ataque
    responses:
      200:
        description: Tipo de ataque encontrado
        schema:
          type: object
      404:
        description: Tipo de ataque não encontrado
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

@attack_type_bp.put("/<int:id>")
def update_attack_type(id):
    """
    Atualizar tipo de ataque
    ---
    tags:
      - AttackTypes
    summary: "Update Attack Type"
    description: "Atualiza as informações de um tipo de ataque existente"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único do tipo de ataque
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - type
          properties:
            type:
              type: string
    responses:
      200:
        description: Tipo de ataque atualizado com sucesso
        schema:
          type: object
      404:
        description: Tipo de ataque não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.json or {}

    type = data.get("type")

    if not type or not isinstance(type, str):
        return {"error": "Invalid type"}, 400
    
    result = service.update(id, type)

    if result is None:
        return {"error": "Not found"}, 404
    
    return result

@attack_type_bp.delete("/<int:id>")
def delete_attack_type(id):
    """
    Deletar tipo de ataque
    ---
    tags:
      - AttackTypes
    summary: "Delete Attack Type"
    description: "Remove um tipo de ataque do sistema"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único do tipo de ataque
    responses:
      204:
        description: Tipo de ataque deletado com sucesso
      404:
        description: Tipo de ataque não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
      409:
        description: Não pode ser deletado (relacionado com outras entidades)
        schema:
          type: object
          properties:
            error:
              type: string
    """
    result = service.delete(id)

    if result is False:
        return {"error": "Not found"}, 404

    if result == "FK":
        return {
            "error": "It cannot be deleted"
        }, 409

    return "", 204