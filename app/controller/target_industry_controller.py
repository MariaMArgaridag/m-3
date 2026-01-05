from flask import Blueprint, request, jsonify
from service.target_industry_service import TargetIndustryService
from repository.target_industry_repository import TargetIndustryRepository
from database import db

target_industry_bp = Blueprint("target_industries", __name__, url_prefix="/target_industries")
service = TargetIndustryService(TargetIndustryRepository(db))

@target_industry_bp.post("/")
def create_target_industry():
    """
    Criar nova indústria alvo
    ---
    tags:
      - TargetIndustries
    summary: "Create Target Industry"
    description: "Registra uma nova indústria/setor que pode ser alvo de ataques"
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
              description: Nome da indústria
              example: "Saúde e Hospitais"
    responses:
      201:
        description: Indústria criada com sucesso
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

    industry = data.get("industry")

    if not industry or not isinstance(industry, str):
        return {"error": "Invalid industry"}, 400

    return jsonify(
        service.create(industry)
    ), 201

@target_industry_bp.get("/")
def list_target_industries():
    """
    Listar todas as indústrias alvo
    ---
    tags:
      - TargetIndustries
    summary: "List All Target Industries"
    description: "Retorna uma lista de todas as indústrias/setores registrados"
    responses:
      200:
        description: Lista de indústrias alvo
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              industry:
                type: string
    """
    return jsonify(service.list())

@target_industry_bp.get("/<int:id>")
def get_by_id_target_industry(id):
    """
    Obter indústria alvo por ID
    ---
    tags:
      - TargetIndustries
    summary: "Read Target Industry"
    description: "Retorna uma indústria específica pelo seu ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único da indústria
    responses:
      200:
        description: Indústria encontrada
        schema:
          type: object
      404:
        description: Indústria não encontrada
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

@target_industry_bp.put("/<int:id>")
def update_target_industry(id):
    """
    Atualizar indústria alvo
    ---
    tags:
      - TargetIndustries
    summary: "Update Target Industry"
    description: "Atualiza as informações de uma indústria existente"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único da indústria
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
    responses:
      200:
        description: Indústria atualizada com sucesso
        schema:
          type: object
      404:
        description: Indústria não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.json or {}

    industry = data.get("industry")

    if not industry or not isinstance(industry, str):
        return {"error": "Invalid industry"}, 400
    
    result = service.update(id, industry)

    if result is None:
        return {"error": "Not found"}, 404
    
    return result

@target_industry_bp.delete("/<int:id>")
def delete_target_industry(id):
    """
    Deletar indústria alvo
    ---
    tags:
      - TargetIndustries
    summary: "Delete Target Industry"
    description: "Remove uma indústria do sistema"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID único da indústria
    responses:
      204:
        description: Indústria deletada com sucesso
      404:
        description: Indústria não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
      409:
        description: Não pode ser deletada (relacionada com outras entidades)
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