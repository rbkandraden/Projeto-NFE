from flask import Blueprint, request, jsonify
from .models import Cliente, db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes/', methods=['POST'])
def criar_cliente():
    data = request.json
    cliente = Cliente(
        nome=data.get('nome'),
        cnpj=data.get('cnpj')
    )
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.to_dict()), 201

@clientes_bp.route('/clientes/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@clientes_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.json
    cliente.nome = data.get('nome', cliente.nome)
    cliente.cnpj = data.get('cnpj', cliente.cnpj)
    db.session.commit()
    return jsonify(cliente.to_dict())

@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente deletado com sucesso."})
