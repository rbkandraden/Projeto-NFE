from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
import xml.etree.ElementTree as ET
from app.models import db, Produto
from datetime import datetime

importa_nfe_bp = Blueprint('importa_nfe', __name__, url_prefix='/nfe')

@importa_nfe_bp.route('/importar', methods=['GET', 'POST'])
@login_required
def importar_xml():
    if request.method == 'POST':
        xml_file = request.files['xmlfile']
        tree = ET.parse(xml_file)
        root = tree.getroot()
        # Exemplo para NF-e 4.00
        for det in root.findall('.//{*}det'):
            prod = det.find('{*}prod')
            cProd = prod.find('{*}cProd').text
            quantidade = int(float(prod.find('{*}qCom').text))
            produto = Produto.query.filter_by(id=int(cProd)).first()
            if produto:
                produto.estoque += quantidade
        db.session.commit()
        flash('NF-e importada e estoque atualizado!', 'success')
        return redirect(url_for('importa_nfe.importar_xml'))
    return render_template('importar_xml.html')