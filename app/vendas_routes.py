from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import db, Venda, Cliente, Produto
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__, url_prefix='/vendas')

# --- Rotas HTML ---

@vendas_bp.route('/', methods=['GET'])
@login_required
def pagina_vendas():
    vendas = Venda.query.all()
    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template('vendas.html', vendas=vendas, clientes=clientes, produtos=produtos)

@vendas_bp.route('/adicionar', methods=['POST'])
def adicionar_venda():
    cliente_id = request.form['cliente_id']
    produto_id = request.form['produto_id']
    quantidade = int(request.form['quantidade'])

    # Validação simples
    if not cliente_id or not produto_id or quantidade <= 0:
        flash('Preencha todos os campos corretamente.', 'danger')
        return redirect(url_for('vendas.pagina_vendas'))

    produto = Produto.query.get(produto_id)
    if not produto:
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('vendas.pagina_vendas'))

    if produto.estoque < quantidade:
        flash('Estoque insuficiente para esta venda.', 'danger')
        return redirect(url_for('vendas.pagina_vendas'))

    produto.estoque -= quantidade
    venda = Venda(cliente_id=cliente_id, produto_id=produto_id, quantidade=quantidade)
    db.session.add(venda)
    db.session.commit()
    flash('Venda registrada com sucesso!', 'success')
    return redirect(url_for('vendas.pagina_vendas'))

# --- Rotas API (JSON) ---

@vendas_bp.route('/api/', methods=['POST'])
def api_adicionar_venda():
    data = request.get_json()
    cliente_id = data.get('cliente_id')
    produto_id = data.get('produto_id')
    quantidade = data.get('quantidade')
    if not cliente_id or not produto_id or not quantidade:
        return jsonify({'error': 'cliente_id, produto_id e quantidade são obrigatórios.'}), 400
    venda = Venda(cliente_id=cliente_id, produto_id=produto_id, quantidade=quantidade)
    db.session.add(venda)
    db.session.commit()
    return jsonify(venda.to_dict()), 201

@vendas_bp.route('/api/', methods=['GET'])
def listar_vendas():
    vendas = Venda.query.all()
    return jsonify([v.to_dict() for v in vendas])

@vendas_bp.route('/api/<int:id>', methods=['PUT'])
def api_editar_venda(id):
    venda = Venda.query.get_or_404(id)
    data = request.get_json()
    venda.cliente_id = data.get('cliente_id', venda.cliente_id)
    venda.produto_id = data.get('produto_id', venda.produto_id)
    venda.quantidade = data.get('quantidade', venda.quantidade)
    db.session.commit()
    return jsonify(venda.to_dict())

@vendas_bp.route('/api/<int:id>', methods=['DELETE'])
def deletar_venda(id):
    venda = Venda.query.get_or_404(id)
    db.session.delete(venda)
    db.session.commit()
    return jsonify({"mensagem": "Venda deletada com sucesso."})

# --- Novas Rotas ---

@vendas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def formulario_venda():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])

        # Validação simples
        if not cliente_id or not produto_id or quantidade <= 0:
            flash('Preencha todos os campos corretamente.', 'danger')
            return redirect(url_for('vendas.formulario_venda'))

        produto = Produto.query.get(produto_id)
        if not produto:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('vendas.formulario_venda'))

        if produto.estoque < quantidade:
            flash('Estoque insuficiente para esta venda.', 'danger')
            return redirect(url_for('vendas.formulario_venda'))

        produto.estoque -= quantidade
        venda = Venda(cliente_id=cliente_id, produto_id=produto_id, quantidade=quantidade)
        db.session.add(venda)
        db.session.commit()
        flash('Venda registrada com sucesso!', 'success')
        return redirect(url_for('vendas.pagina_vendas'))

    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template('formulario_venda.html', clientes=clientes, produtos=produtos)

@vendas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_venda(id):
    venda = Venda.query.get_or_404(id)

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])

        # Validação simples
        if not cliente_id or not produto_id or quantidade <= 0:
            flash('Preencha todos os campos corretamente.', 'danger')
            return redirect(url_for('vendas.editar_venda', id=id))

        produto = Produto.query.get(produto_id)
        if not produto:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('vendas.editar_venda', id=id))

        # Atualiza apenas se o estoque permitir
        if produto.estoque + venda.quantidade < quantidade:
            flash('Estoque insuficiente para esta venda.', 'danger')
            return redirect(url_for('vendas.editar_venda', id=id))

        # Restaura o estoque anterior
        produto_antigo = Produto.query.get(venda.produto_id)
        produto_antigo.estoque += venda.quantidade

        produto.estoque -= quantidade
        venda.cliente_id = cliente_id
        venda.produto_id = produto_id
        venda.quantidade = quantidade
        db.session.commit()
        flash('Venda atualizada com sucesso!', 'success')
        return redirect(url_for('vendas.pagina_vendas'))

    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template('editar_venda.html', venda=venda, clientes=clientes, produtos=produtos)

@vendas_bp.route('/excluir/<int:id>', methods=['POST', 'GET'])
@login_required
def excluir_venda(id):
    venda = Venda.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(venda)
        db.session.commit()
        flash('Venda excluída com sucesso!', 'success')
        return redirect(url_for('vendas.pagina_vendas'))

    return render_template('excluir_venda.html', venda=venda)
