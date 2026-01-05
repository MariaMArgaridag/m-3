from flask import Flask, jsonify, render_template, request
from flasgger import Swagger
import json
from controller.attack_type_controller import attack_type_bp
from controller.attack_controller import attack_bp
from controller.cyber_threat_controller import cyber_threat_bp
from controller.defense_mechanism_controller import defense_mechanism_bp
from controller.security_vulnerability_controller import security_vulnerability_bp
from controller.target_industry_controller import target_industry_bp

app = Flask(__name__, template_folder='templates')

# Configuração do Flasgger (Swagger UI) - Design moderno similar a FastAPI
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": False,
    "ui": ["swagger", "rapidoc"],
    "favicon": "https://fastapi.tiangolo.com/img/favicon.png"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Cybersecurity Threats API",
        "description": "API REST para gerenciamento de ameaças de cibersegurança. Arquitetura de 4 camadas (Controller → Service → Repository → Database)",
        "version": "1.0.0",
        "x-logo": {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
            "altText": "Cybersecurity API"
        },
        "contact": {
            "name": "API Support",
            "email": "support@cybersecurity-api.com"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {
            "name": "DefenseMechanisms",
            "description": "🛡️ Gerenciamento de Mecanismos de Defesa - Criar, listar, atualizar e deletar defesas",
            "externalDocs": {
                "description": "Documentação completa",
                "url": "https://example.com/docs/defense"
            }
        },
        {
            "name": "Attacks",
            "description": "🔓 Gerenciamento de Ataques - Operações CRUD e estatísticas de ataques cibernéticos",
            "externalDocs": {
                "description": "Documentação completa",
                "url": "https://example.com/docs/attacks"
            }
        },
        {
            "name": "SecurityVulnerabilities",
            "description": "⚠️ Gerenciamento de Vulnerabilidades - Monitoramento e registro de vulnerabilidades de segurança",
            "externalDocs": {
                "description": "Documentação completa",
                "url": "https://example.com/docs/vulnerabilities"
            }
        },
        {
            "name": "CyberThreats",
            "description": "🚨 Gerenciamento de Ameaças - Registro e análise de incidentes de cibersegurança",
            "externalDocs": {
                "description": "Documentação completa",
                "url": "https://example.com/docs/threats"
            }
        },
        {
            "name": "AttackTypes",
            "description": "📋 Tipos de Ataques - Classificação e categorização de ataques",
        },
        {
            "name": "TargetIndustries",
            "description": "🏢 Indústrias Alvo - Setores e indústrias sob foco de ataques",
        }
    ]
}

# Inicializar Swagger com Flasgger
swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Função para limpar operationId (deixar mais elegante visualmente)
@app.after_request
def clean_operation_ids(response):
    """Remove operationId da especificação Swagger para uma interface mais elegante"""
    if 'apispec.json' in request.path and 'application/json' in response.content_type:
        try:
            spec = response.get_json()
            if spec and 'paths' in spec:
                for path in spec['paths'].values():
                    for method in ['get', 'post', 'put', 'delete', 'patch', 'options']:
                        if method in path and isinstance(path[method], dict):
                            # Remove operationId mas mantém outras propriedades
                            path[method].pop('operationId', None)
            response.data = json.dumps(spec).encode('utf-8')
        except Exception:
            pass  # Se falhar, mantém a resposta original
    return response

# Registrar blueprints
app.register_blueprint(attack_type_bp)
app.register_blueprint(attack_bp)
app.register_blueprint(cyber_threat_bp)
app.register_blueprint(defense_mechanism_bp)
app.register_blueprint(security_vulnerability_bp)
app.register_blueprint(target_industry_bp)

# Rota raiz - Mensagem de boas-vindas
@app.route("/", methods=["GET"])
def welcome():
    """
    Rota de boas-vindas da API
    ---
    tags:
      - Welcome
    responses:
      200:
        description: Mensagem de boas-vindas
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Bem-vindos à nossa API. Digite a rota desejada!"
            documentation:
              type: string
              example: "/apidocs"
            available_routes:
              type: object
              properties:
                defenses:
                  type: string
                  example: "/defense_mechanisms"
                attacks:
                  type: string
                  example: "/attacks"
                vulnerabilities:
                  type: string
                  example: "/security_vulnerabilities"
                incidents:
                  type: string
                  example: "/cyber_threats"
    """
    return jsonify({
        "message": "API REST. Arquitetura de 4 camadas: OK!",
        "documentation": "/apidocs",
        "available_routes": {
            "defenses": "/defense_mechanisms",
            "attacks": "/attacks",
            "vulnerabilities": "/security_vulnerabilities",
            "incidents": "/cyber_threats",
            "attack_types": "/attack_types",
            "target_industries": "/target_industries"
        }
    }), 200

# Rota customizada para servir o template Swagger bonito
@app.route("/apidocs", methods=["GET"])
def custom_swagger_ui():
    """
    Interface Swagger UI customizada e modernizada
    """
    return render_template('swagger_ui.html')

if __name__ == "__main__":
    app.run(debug=True)