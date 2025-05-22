from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from .models import Cliente, db

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

# --- Rotas HTML ---

@clientes_bp.route('/', methods=['GET'])
def pagina_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@clientes_bp.route('/adicionar', methods=['POST'])
def adicionar_cliente():
    nome = request.form.get('nome')
    cnpj = request.form.get('cnpj')

    if not nome or not cnpj:
        flash('Nome e CNPJ são obrigatórios.', 'error')
        return redirect(url_for('clientes.pagina_clientes'))

    cliente = Cliente(nome=nome, cnpj=cnpj)
    db.session.add(cliente)
    db.session.commit()
    flash('Cliente adicionado com sucesso!', 'success')
    return redirect(url_for('clientes.pagina_clientes'))

# --- Rotas API (JSON) ---

@clientes_bp.route('/api/', methods=['POST'])
def criar_cliente():
    data = request.json
    cliente = Cliente(
        nome=data.get('nome'),
        cnpj=data.get('cnpj')
    )
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.to_dict()), 201

@clientes_bp.route('/api/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@clientes_bp.route('/api/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.json
    cliente.nome = data.get('nome', cliente.nome)
    cliente.cnpj = data.get('cnpj', cliente.cnpj)
    db.session.commit()
    return jsonify(cliente.to_dict())

@clientes_bp.route('/api/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente deletado com sucesso."})
