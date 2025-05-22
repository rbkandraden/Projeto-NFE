from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Para usar flash messages nos templates
    app.secret_key = 'sua_chave_secreta_aqui'  # substitua por uma chave segura

    db.init_app(app)
    migrate.init_app(app, db)

    # Rotas principais
    from .routes import main
    app.register_blueprint(main)

    # Módulos do sistema
    from .produtos_routes import produtos_bp
    app.register_blueprint(produtos_bp)

    from .clientes_routes import clientes_bp
    app.register_blueprint(clientes_bp)

    from .vendas_routes import vendas_bp
    app.register_blueprint(vendas_bp)

    from .pagamentos_routes import pagamentos_bp
    app.register_blueprint(pagamentos_bp)

    return app
