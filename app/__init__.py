from flask import Flask, jsonify #Cria a aplicação Web

from config import Config
from .extensions import db
from .routes import users_bp

def create_app(): #Cria a aplicação Flask (Application Factory)
    app = Flask(__name__) #__name__ ajuda o Flask a localizar arquivos e recursos do projeto
    app.config.from_object(Config) #Carrega as configurações do arquivo config.py

    db.init_app(app) #Liga o SQLAlchemy à aplicação Flask

    app.json.sort_keys = False

    app.register_blueprint(users_bp) #Aqui o Flask registra todas as rotas definidas no routes.py

    @app.get("/") #Cria uma rota simples: GET /; e como resposta recebe: 
    def home():
        return jsonify({"message": "API de gerenciamento de usuários funcionando!"})
    
    with app.app_context():
        db.create_all() #CREATE TABLE users (...)

    return app