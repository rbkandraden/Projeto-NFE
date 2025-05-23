from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from .models import Cliente, db

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

# --- Rotas HTML ---

@clientes_bp.route('/', methods=['GET'])
@login_required
def pagina_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@clientes_bp.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form.get('nome')
    email = request.form.get('email')
    cnpj = request.form.get('cnpj')
    if not nome or not email:
        flash('Nome e email são obrigatórios.', 'danger')
        return redirect(url_for('clientes.pagina_clientes'))
    cliente = Cliente(nome=nome, email=email, cnpj=cnpj)
    db.session.add(cliente)
    db.session.commit()
    flash('Cliente cadastrado com sucesso!', 'success')
    return redirect(url_for('clientes.pagina_clientes'))

@clientes_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def formulario_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cnpj = request.form['cnpj']

        # Validação simples
        if not nome or not email:
            flash('Nome e e-mail são obrigatórios.', 'danger')
            return redirect(url_for('clientes.formulario_cliente'))

        # (Opcional) Validação de formato de e-mail e CNPJ pode ser adicionada aqui

        novo = Cliente(nome=nome, email=email, cnpj=cnpj)
        db.session.add(novo)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('clientes.pagina_clientes'))
    return render_template('cliente_form.html')

@clientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.email = request.form['email']
        cliente.cnpj = request.form['cnpj']

        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clientes.pagina_clientes'))
    return render_template('editar_cliente.html', cliente=cliente)

@clientes_bp.route('/excluir/<int:id>', methods=['POST', 'GET'])
@login_required
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente excluído com sucesso!', 'success')
        return redirect(url_for('clientes.pagina_clientes'))
    return render_template('excluir_cliente.html', cliente=cliente)

# --- Rotas API (JSON) ---

@clientes_bp.route('/api/', methods=['POST'])
def api_adicionar_cliente():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    cnpj = data.get('cnpj')
    if not nome or not email:
        return jsonify({'error': 'Nome e email são obrigatórios.'}), 400
    cliente = Cliente(nome=nome, email=email, cnpj=cnpj)
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.to_dict()), 201

@clientes_bp.route('/api/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@clientes_bp.route('/api/<int:id>', methods=['PUT'])
def api_editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()
    cliente.nome = data.get('nome', cliente.nome)
    cliente.email = data.get('email', cliente.email)
    cliente.cnpj = data.get('cnpj', cliente.cnpj)
    db.session.commit()
    return jsonify(cliente.to_dict())

@clientes_bp.route('/api/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente deletado com sucesso."})
