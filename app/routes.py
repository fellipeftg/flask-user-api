# Esse arquivo é o coração da API
# Aqui são definidas as rotas que executam o CRUD no banco de dados
# É o controlador da aplicação; ele recebe requisições HTTP, conversa com o banco e retorna respostas em JSON

from flask import Blueprint, jsonify, request #"Blueprint": organiza rotas e módulos
from sqlalchemy import select #SELECT * FROM users
from sqlalchemy.exc import IntegrityError #Captura erros no DB

from .extensions import db
from .models import User

users_bp = Blueprint("users", __name__, url_prefix="/users") #Todas as rotas daqui terão prefixo "/users"

@users_bp.post("")
def create_user():
    data = request.get_json(silent=True) or {} #"(silent=True)" -> se a requisição não tiver JSON válido, não lance erro e caso retorne None, lance um dicionário vazio "{}"
    name = data.get("name", "").strip() #As aspas servem para dizer que na falta de tal chave, retoner uma Str vazia
    email = data.get("email", "").strip().lower()

    if not name or not email:
        return jsonify({"error": "Os campos 'name' e 'email' são obrigatórios!"}), 400 #Bad Request
    
    user = User(name=name, email=email)
    db.session.add(user) #Cria objeto e adiciona à sessão do banco

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error:": "Esse email já está cadastrado!"}), 409 #Conflict
    
    return jsonify(user.to_dict()), 201 #Created

@users_bp.get("")
def list_users():
    users = db.session.execute(
        select(User).order_by(User.id)
    ).scalars().all()

    return jsonify([user.to_dict() for user in users]), 200

@users_bp.get("/<int:user_id>")
def get_user(user_id):
    user = db.session.get(User, user_id) #SELECT * FROM users WHERE id = 1

    if not user:
        return jsonify({"error:": "Usuário não encontrado!"}), 404 #Not Found
    
    return jsonify(user.to_dict()), 201

@users_bp.put("/<int:user_id>")
def update_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    data = request.get_json(silent=True) or {}

    if "name" in data:
        name = str(data["name"]).strip()
        if not name:
            return jsonify({"error": "O campo 'name' não pode ser vazio."}), 400
        user.name = name

    if "email" in data:
        email = str(data["email"]).strip().lower()
        if not email:
            return jsonify({"error": "O campo 'email' não pode ser vazio."}), 400
        user.email = email

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Este e-mail já está cadastrado."}), 409

    return jsonify(user.to_dict()), 200

@users_bp.delete("<int:user_id>")
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error:": 'Usuário não encontrado!'}), 404
    
    db.session.delete(user)
    db.session.commit() #DELETE FROM users WHERE id = 1

    return jsonify({"message:": "Usuário deletado com sucesso!"})