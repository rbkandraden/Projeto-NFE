from . import db
from datetime import datetime

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "estoque": self.estoque
        }

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj
        }

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float)
    status_nf = db.Column(db.String(20), default='pendente')

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "data": self.data.isoformat(),
            "total": self.total,
            "status_nf": self.status_nf
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
