from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from .models import Venda, Cliente, Produto, db
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__, url_prefix='/vendas')

# --- Rotas HTML ---

@vendas_bp.route('/', methods=['GET'])
def pagina_vendas():
    vendas = Venda.query.all()
    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template('vendas.html', vendas=vendas, clientes=clientes, produtos=produtos)

@vendas_bp.route('/adicionar', methods=['POST'])
def adicionar_venda():
    cliente_id = request.form.get('cliente_id')
    produto_id = request.form.get('produto_id')
    quantidade = request.form.get('quantidade')

    if not cliente_id or not produto_id or not quantidade:
        flash('Todos os campos são obrigatórios.', 'error')
        return redirect(url_for('vendas.pagina_vendas'))

    # Para calcular total, pega o preço do produto
    produto = Produto.query.get(produto_id)
    if not produto:
        flash('Produto inválido.', 'error')
        return redirect(url_for('vendas.pagina_vendas'))

    total = produto.preco * int(quantidade)

    venda = Venda(
        cliente_id=int(cliente_id),
        total=total,
        status_nf='pendente',
        data=datetime.now().date()
    )
    db.session.add(venda)
    db.session.commit()
    flash('Venda registrada com sucesso!', 'success')
    return redirect(url_for('vendas.pagina_vendas'))

# --- Rotas API (JSON) ---

@vendas_bp.route('/api/', methods=['POST'])
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

@vendas_bp.route('/api/', methods=['GET'])
def listar_vendas():
    vendas = Venda.query.all()
    return jsonify([v.to_dict() for v in vendas])

@vendas_bp.route('/api/<int:id>', methods=['PUT'])
def atualizar_venda(id):
    venda = Venda.query.get_or_404(id)
    data = request.json
    venda.total = data.get('total', venda.total)
    venda.status_nf = data.get('status_nf', venda.status_nf)
    db.session.commit()
    return jsonify(venda.to_dict())

@vendas_bp.route('/api/<int:id>', methods=['DELETE'])
def deletar_venda(id):
    venda = Venda.query.get_or_404(id)
    db.session.delete(venda)
    db.session.commit()
    return jsonify({"mensagem": "Venda deletada com sucesso."})
