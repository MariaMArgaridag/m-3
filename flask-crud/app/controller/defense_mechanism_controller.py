
#novo
from flask import Blueprint, request, jsonify
from app.service.defense_mechanism_service import DefenseMechanismService
from app.repository.defense_mechanism_repository import DefenseMechanismRepository
from app.database import db

# Blueprint: tudo o que estiver aqui começa com /defense_mechanisms
defense_mechanism_bp = Blueprint(
    "defense_mechanisms",
    __name__,
    url_prefix="/defense_mechanisms"
)

# Liga Camada 1 -> Camada 2 (service) -> Camada 3 (repository)
service = DefenseMechanismService(DefenseMechanismRepository(db))


@defense_mechanism_bp.post("/")
def create_defense_mechanism():
    """
    Cria um novo mecanismo de defesa
    ---
    tags:
      - Defense Mechanisms
    consumes:
      - application/json
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
              example: Firewall
    responses:
      201:
        description: Mecanismo criado
      400:
        description: Dados inválidos
    """
    data = request.json or {}

    mechanism = data.get("mechanism")

    if not mechanism or not isinstance(mechanism, str):
        return jsonify({"error": "Mechanism invalid"}), 400

    created = service.create(mechanism)
    return jsonify(created), 201


@defense_mechanism_bp.get("/")
def list_defense_mechanisms():
    """
    Lista todos os mecanismos de defesa
    ---
    tags:
      - Defense Mechanisms
    responses:
      200:
        description: Lista de mecanismos de defesa
    """
    return jsonify(service.list()), 200


@defense_mechanism_bp.get("/<int:id>")
def get_by_id_defense_mechanism(id):
    """
    Obtém um mecanismo de defesa pelo ID
    ---
    tags:
      - Defense Mechanisms
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Mecanismo encontrado
      404:
        description: Não encontrado
    """
    result = service.get_by_id(id)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(result), 200


@defense_mechanism_bp.put("/<int:id>")
def update_defense_mechanism(id):
    """
    Atualiza um mecanismo de defesa pelo ID
    ---
    tags:
      - Defense Mechanisms
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
            - mechanism
          properties:
            mechanism:
              type: string
              example: VPN
    responses:
      200:
        description: Mecanismo atualizado
      400:
        description: Dados inválidos
      404:
        description: Não encontrado
    """
    data = request.json or {}

    mechanism = data.get("mechanism")

    if not mechanism or not isinstance(mechanism, str):
        return jsonify({"error": "Mechanism invalid"}), 400

    result = service.update(id, mechanism)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(result), 200


@defense_mechanism_bp.delete("/<int:id>")
def delete_defense_mechanism(id):
    """
    Apaga um mecanismo de defesa pelo ID
    ---
    tags:
      - Defense Mechanisms
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

    if result == "FK":
        return jsonify({"error": "It cannot be deleted"}), 409

    return "", 204
