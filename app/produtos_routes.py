from flask import Blueprint, request, jsonify
from app import db
from app.models import Produto

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([p.to_dict() for p in produtos])

@produtos_bp.route('/', methods=['POST'])
def criar_produto():
    data = request.get_json()
    produto = Produto(
        nome=data['nome'],
        preco=data['preco'],
        estoque=data.get('estoque', 0)
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify(produto.to_dict()), 201

@produtos_bp.route('/<int:id>', methods=['GET'])
def obter_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify(produto.to_dict())

@produtos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    data = request.get_json()
    produto.nome = data.get('nome', produto.nome)
    produto.preco = data.get('preco', produto.preco)
    produto.estoque = data.get('estoque', produto.estoque)
    db.session.commit()
    return jsonify(produto.to_dict())

@produtos_bp.route('/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return '', 204
