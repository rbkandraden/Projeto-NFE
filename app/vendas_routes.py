from flask import Blueprint, request, jsonify
from .models import Venda, db

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/vendas/', methods=['POST'])
def criar_venda():
    data = request.json
    venda = Venda(
        cliente_id=data.get('cliente_id'),
        total=data.get('total'),
        status_nf=data.get('status_nf', 'pendente')
    )
    db.session.add(venda)
    db.session.commit()
    return jsonify(venda.to_dict()), 201

@vendas_bp.route('/vendas/', methods=['GET'])
def listar_vendas():
    vendas = Venda.query.all()
    return jsonify([v.to_dict() for v in vendas])

@vendas_bp.route('/vendas/<int:id>', methods=['PUT'])
def atualizar_venda(id):
    venda = Venda.query.get_or_404(id)
    data = request.json
    venda.total = data.get('total', venda.total)
    venda.status_nf = data.get('status_nf', venda.status_nf)
    db.session.commit()
    return jsonify(venda.to_dict())

@vendas_bp.route('/vendas/<int:id>', methods=['DELETE'])
def deletar_venda(id):
    venda = Venda.query.get_or_404(id)
    db.session.delete(venda)
    db.session.commit()
    return jsonify({"mensagem": "Venda deletada com sucesso."})
