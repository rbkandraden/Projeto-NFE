from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import Pagamento, db

pagamentos_bp = Blueprint('pagamentos', __name__)

@pagamentos_bp.route('/pagamentos/', methods=['POST'])
def criar_pagamento():
    data = request.json

    # Converte string para objeto date
    data_pagamento = datetime.strptime(data.get('data'), "%Y-%m-%d").date()

    pagamento = Pagamento(
        venda_id=data.get('venda_id'),
        valor=data.get('valor'),
        data=data_pagamento,
        quitado=data.get('quitado', False)
    )
    db.session.add(pagamento)
    db.session.commit()
    return jsonify(pagamento.to_dict()), 201

@pagamentos_bp.route('/pagamentos/', methods=['GET'])
def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    return jsonify([p.to_dict() for p in pagamentos])

@pagamentos_bp.route('/pagamentos/<int:id>', methods=['PUT'])
def atualizar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    data = request.json

    pagamento.valor = data.get('valor', pagamento.valor)
    
    # Converte, se fornecido, a nova data como objeto date
    if 'data' in data:
        pagamento.data = datetime.strptime(data['data'], "%Y-%m-%d").date()

    pagamento.quitado = data.get('quitado', pagamento.quitado)
    
    db.session.commit()
    return jsonify(pagamento.to_dict())

@pagamentos_bp.route('/pagamentos/<int:id>', methods=['DELETE'])
def deletar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({"mensagem": "Pagamento deletado com sucesso."})
