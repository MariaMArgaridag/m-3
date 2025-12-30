

#novo codigo 

from flask import Blueprint, request, jsonify
from app.service.attack_type_service import AttackTypeService
from app.repository.attack_type_repository import AttackTypeRepository
from app.database import db

# Blueprint: tudo o que estiver aqui vai começar com /attack_types
attack_type_bp = Blueprint("attack_types", __name__, url_prefix="/attack_types")

# Liga Camada 1 -> Camada 2 (service) -> Camada 3 (repository)
service = AttackTypeService(AttackTypeRepository(db))


@attack_type_bp.post("/")
def create_attack_type():
    """
    Cria um novo tipo de ataque
    ---
    tags:
      - Attack Types
    consumes:
      - application/json
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
              example: DDoS
    responses:
      201:
        description: Tipo de ataque criado
      400:
        description: Dados inválidos
    """
    data = request.json or {}

    # Evitar usar "type" como variável (é nome reservado do Python)
    attack_type_name = data.get("type")

    # Validação simples (Camada 1): tem de existir e ser string
    if not attack_type_name or not isinstance(attack_type_name, str):
        return jsonify({"error": "Invalid type"}), 400

    created = service.create(attack_type_name)
    return jsonify(created), 201


@attack_type_bp.get("/")
def list_attack_types():
    """
    Lista todos os tipos de ataque
    ---
    tags:
      - Attack Types
    responses:
      200:
        description: Lista de tipos de ataque
    """
    return jsonify(service.list()), 200


@attack_type_bp.get("/<int:id>")
def get_by_id_attack_type(id):
    """
    Obtém um tipo de ataque pelo ID
    ---
    tags:
      - Attack Types
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Tipo de ataque encontrado
      404:
        description: Não encontrado
    """
    result = service.get_by_id(id)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(result), 200


@attack_type_bp.put("/<int:id>")
def update_attack_type(id):
    """
    Atualiza um tipo de ataque pelo ID
    ---
    tags:
      - Attack Types
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
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
              example: Malware
    responses:
      200:
        description: Tipo de ataque atualizado
      400:
        description: Dados inválidos
      404:
        description: Não encontrado
    """
    data = request.json or {}
    attack_type_name = data.get("type")

    if not attack_type_name or not isinstance(attack_type_name, str):
        return jsonify({"error": "Invalid type"}), 400

    result = service.update(id, attack_type_name)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(result), 200


@attack_type_bp.delete("/<int:id>")
def delete_attack_type(id):
    """
    Apaga um tipo de ataque pelo ID
    ---
    tags:
      - Attack Types
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
    responses:
      204:
        description: Apagado com sucesso
      404:
        description: Não encontrado
      409:
        description: Não pode ser apagado (FK)
    """
    result = service.delete(id)

    if result is False:
        return jsonify({"error": "Not found"}), 404

    # Se a Camada 3 disser que está ligado por FK, devolvemos 409
    if result == "FK":
        return jsonify({"error": "It cannot be deleted"}), 409

    return "", 204
