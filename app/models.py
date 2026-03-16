from datetime import datetime, timezone
from .extensions import db

class User(db.Model): #Modelo ORM; representa uma table no DB
    _tablename_ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable = False) #"nullable" mesmo que NOT NULL
    email = db.Column(db.String(80), unique = True, nullable = False, index = True) #index = True; melhora a velocidade de busca

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default=lambda: datetime.now(timezone.utc) #quando o usuário for criado, o DB salva automaticamente a data atual.
    ) #created_at TIMESTAMP

    def to_dict(self): #transforma o objeto Python em dicionário, que depois vira JSON na API.
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() #.isoformat() converte um objeto de data e hora (datetime) do Python em uma string
        }