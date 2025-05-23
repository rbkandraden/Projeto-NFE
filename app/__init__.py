from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Registre todos os blueprints
    from .auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from .routes import main
    app.register_blueprint(main)

    from .produtos_routes import produtos_bp
    app.register_blueprint(produtos_bp)

    from .clientes_routes import clientes_bp
    app.register_blueprint(clientes_bp)

    from .vendas_routes import vendas_bp
    app.register_blueprint(vendas_bp)

    from .pagamentos_routes import pagamentos_bp
    app.register_blueprint(pagamentos_bp)

    from .index import index_bp
    app.register_blueprint(index_bp)

    from .importa_nfe_routes import importa_nfe_bp
    app.register_blueprint(importa_nfe_bp)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import Usuario  # Importa Usuario só aqui, para evitar ciclo
        return Usuario.query.get(int(user_id))

    return app
