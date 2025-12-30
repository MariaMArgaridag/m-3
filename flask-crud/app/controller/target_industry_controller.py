

#novo

from flask import Blueprint, request, jsonify
from app.service.target_industry_service import TargetIndustryService
from app.repository.target_industry_repository import TargetIndustryRepository
from app.database import db

# Blueprint: tudo o que estiver aqui começa com /target_industries
target_industry_bp = Blueprint(
    "target_industries",
    __name__,
    url_prefix="/target_industries"
)

# Liga Camada 1 -> Camada 2 (service) -> Camada 3 (repository)
service = TargetIndustryService(TargetIndustryRepository(db))


@target_industry_bp.post("/")
def create_target_industry():
    """
    Cria uma nova indústria alvo
    ---
    tags:
      - Target Industries
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - industry
          properties:
            industry:
              type: string
              example: Banking
    responses:
      201:
        description: Indústria criada
      400:
        description: Dados inválidos
    """
    data = request.json or {}

    industry = data.get("industry")

    if not industry or not isinstance(industry, str):
        return jsonify({"error": "Invalid industry"}), 400

    created = service.create(industry)
    return jsonify(created), 201


@target_industry_bp.get("/")
def list_target_industries():
    """
    Lista todas as indústrias alvo
    ---
    tags:
      - Target Industries
    responses:
      200:
        description: Lista de indústrias
    """
    return jsonify(service.list()), 200


@target_industry_bp.get("/<int:id>")
def get_by_id_target_industry(id):
    """
    Obtém uma indústria alvo pelo ID
    ---
    tags:
      - Target Industries
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Indústria encontrada
      404:
        description: Não encontrada
    """
    result = service.get_by_id(id)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(result), 200


@target_industry_bp.put("/<int:id>")
def update_target_industry(id):
    """
    Atualiza uma indústria alvo pelo ID
    ---
    tags:
      - Target Industries
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
            - industry
          properties:
            industry:
              type: string
              example: Healthcare
    responses:
      200:
        description: Indústria atualizada
      400:
        description: Dados inválidos
      404:
        description: Não encontrada
    """
    data = request.json or {}

    industry = data.get("industry")

    if not industry or not isinstance(industry, str):
        return jsonify({"error": "Invalid industry"}), 400

    result = service.update(id, industry)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(result), 200


@target_industry_bp.delete("/<int:id>")
def delete_target_industry(id):
    """
    Apaga uma indústria alvo pelo ID
    ---
    tags:
      - Target Industries
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
    responses:
      204:
        description: Apagada com sucesso
      404:
        description: Não encontrada
      409:
        description: Não pode ser apagada (FK)
    """
    result = service.delete(id)

    if result is False:
        return jsonify({"error": "Not found"}), 404

    if result == "FK":
        return jsonify({"error": "It cannot be deleted"}), 409

    return "", 204
