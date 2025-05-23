from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime
from flask_login import UserMixin

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    marca = db.Column(db.String(80), nullable=True)  # Adicione esta linha
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    estoque_minimo = db.Column(db.Integer, nullable=False, default=0)  # Novo campo

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "marca": self.marca,  # Inclua a marca aqui
            "preco": self.preco,
            "estoque": self.estoque
        }

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cnpj = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cnpj": self.cnpj
        }

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', backref='vendas')
    produto = db.relationship('Produto', backref='vendas')

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "data": self.data.isoformat()
        }

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'))
    valor = db.Column(db.Float)
    data = db.Column(db.Date)
    quitado = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "venda_id": self.venda_id,
            "valor": self.valor,
            "data": self.data.isoformat(),
            "quitado": self.quitado
        }

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)


