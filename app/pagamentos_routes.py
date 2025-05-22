from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
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
def pagina_pagamentos():
    pagamentos = Pagamento.query.order_by(Pagamento.data.desc()).all()
    return render_template('pagamentos.html', pagamentos=pagamentos)

@pagamentos_bp.route('/novo', methods=['GET', 'POST'])
def formulario_pagamento():
    if request.method == 'POST':
        try:
            venda_id = int(request.form['venda_id'])
            valor = float(request.form['valor'])
            data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
            quitado = 'quitado' in request.form

            novo_pagamento = Pagamento(
                venda_id=venda_id,
                valor=valor,
                data=data,
                quitado=quitado
            )
            db.session.add(novo_pagamento)
            db.session.commit()
            flash('Pagamento registrado com sucesso!', 'success')
            return redirect(url_for('pagamentos.pagina_pagamentos'))

        except Exception as e:
            flash(f'Erro ao salvar pagamento: {e}', 'danger')
            return redirect(url_for('pagamentos.formulario_pagamento'))

    return render_template('pagamento_form.html')
