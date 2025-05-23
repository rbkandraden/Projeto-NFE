from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models import Produto
from flask_login import login_required

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

# ====================
# === ROTAS - JSON ===
# ====================

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

# ===========================
# === ROTAS - TEMPLATE HTML
# ===========================

@produtos_bp.route('/lista', methods=['GET'])
@login_required
def pagina_produtos():
    baixo_estoque = request.args.get('baixo_estoque')
    if baixo_estoque:
        produtos = Produto.query.filter(Produto.estoque <= Produto.estoque_minimo).all()
    else:
        produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@produtos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def formulario_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']  # Captura a marca
        preco = float(request.form['preco'])
        estoque = int(request.form['estoque'])
        estoque_minimo = int(request.form['estoque_minimo'])
        if not nome or not marca or preco < 0 or estoque < 0 or estoque_minimo < 0:
            flash('Preencha todos os campos corretamente!', 'danger')
            return redirect(url_for('produtos.formulario_produto'))
        novo = Produto(
            nome=nome,
            marca=marca,  # Salva a marca
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo
        )
        db.session.add(novo)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos.pagina_produtos'))
    return render_template('produto_form.html')

@produtos_bp.route('/estoque')
@login_required
def saldo_estoque():
    produtos = Produto.query.all()
    return render_template('estoque.html', produtos=produtos)

@produtos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.marca = request.form['marca']  # Atualiza a marca
        produto.preco = float(request.form['preco'])
        produto.estoque = int(request.form['estoque'])
        produto.estoque_minimo = int(request.form['estoque_minimo'])
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos.pagina_produtos'))
    return render_template('produto_form.html', produto=produto)

@produtos_bp.route('/verifica_estoque/<int:produto_id>/<int:quantidade>', methods=['GET'])
def verifica_estoque(produto_id, quantidade):
    produto = Produto.query.get(produto_id)
    if produto.estoque < quantidade:
        flash('Estoque insuficiente para esta venda.', 'danger')
        return redirect(url_for('vendas.pagina_vendas'))
    produto.estoque -= quantidade
    db.session.commit()
    # Lógica para prosseguir com a venda
    return redirect(url_for('vendas.pagina_vendas'))
