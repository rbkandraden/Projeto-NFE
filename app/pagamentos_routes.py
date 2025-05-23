from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from .models import Pagamento, db

pagamentos_bp = Blueprint('pagamentos', __name__, url_prefix='/pagamentos')

# ====================
# === ROTAS - JSON ===
# ====================

@pagamentos_bp.route('/', methods=['POST'])
def criar_pagamento():
    data = request.json
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

@pagamentos_bp.route('/', methods=['GET'])
def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    return jsonify([p.to_dict() for p in pagamentos])

@pagamentos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    data = request.json

    pagamento.valor = data.get('valor', pagamento.valor)
    if 'data' in data:
        pagamento.data = datetime.strptime(data['data'], "%Y-%m-%d").date()
    pagamento.quitado = data.get('quitado', pagamento.quitado)

    db.session.commit()
    return jsonify(pagamento.to_dict())

@pagamentos_bp.route('/<int:id>', methods=['DELETE'])
def deletar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({"mensagem": "Pagamento deletado com sucesso."})

# ===========================
# === ROTAS - TEMPLATE HTML
# ===========================

@pagamentos_bp.route('/lista', methods=['GET'])
@login_required
def pagina_pagamentos():
    pagamentos = Pagamento.query.order_by(Pagamento.data.desc()).all()
    return render_template('pagamentos.html', pagamentos=pagamentos)

@pagamentos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def formulario_pagamento():
    if request.method == 'POST':
        venda_id = request.form['venda_id']
        valor = float(request.form['valor'])
        quitado = request.form.get('quitado') == 'True'

        # Validação simples
        if not venda_id or valor <= 0:
            flash('Preencha todos os campos corretamente.', 'danger')
            return redirect(url_for('pagamentos.formulario_pagamento'))

        novo = Pagamento(venda_id=venda_id, valor=valor, quitado=quitado)
        db.session.add(novo)
        db.session.commit()
        flash('Pagamento registrado com sucesso!', 'success')
        return redirect(url_for('pagamentos.pagina_pagamentos'))
    return render_template('pagamento_form.html')

@pagamentos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)

    if request.method == 'POST':
        pagamento.valor = request.form['valor']
        pagamento.quitado = request.form.get('quitado') == 'True'

        db.session.commit()
        flash('Pagamento atualizado com sucesso!', 'success')
        return redirect(url_for('pagamentos.pagina_pagamentos'))

    return render_template('pagamento_edit.html', pagamento=pagamento)

@pagamentos_bp.route('/excluir/<int:id>', methods=['POST', 'GET'])
@login_required
def excluir_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(pagamento)
        db.session.commit()
        flash('Pagamento excluído com sucesso!', 'success')
        return redirect(url_for('pagamentos.pagina_pagamentos'))

    return render_template('pagamento_excluir.html', pagamento=pagamento)

@pagamentos_bp.route('/estoque')
def saldo_estoque():
    produtos = Produto.query.order_by(Produto.marca, Produto.nome).all()
    return render_template('estoque.html', produtos=produtos)
