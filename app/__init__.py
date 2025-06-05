from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # Importar Flask-Bcrypt
from flask_login import LoginManager # Importar Flask-Login
import os

db = SQLAlchemy() # Inicializa o SQLAlchemy
bcrypt = Bcrypt() # Inicializa Bcrypt
login_manager = LoginManager() # Inicializa LoginManager
login_manager.login_view = 'main.login_render' # Define a rota para redirecionar se o login for obrigatório
login_manager.login_message_category = 'info' # Categoria da mensagem flash para login requerido

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_forte_e_aleatoria_aqui_em_producao_leia_de_variavel_de_ambiente' # Mudar em produção!
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_file_path = os.path.join(project_root, 'db', 'ecommerce_db.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'
    print(f"DEBUG: SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"DEBUG: Tentando criar DB em: {db_file_path}")

    db.init_app(app) # Associa o db à instância do app
    bcrypt.init_app(app) # Associa o bcrypt ao app
    login_manager.init_app(app) # Associa o login_manager ao app

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Blueprints importados aqui
    from app.routes import auth_bp

    app.register_blueprint(auth_bp)
    # Importe os modelos APÓS db.init_app(app)
    # Importar aqui garante que os modelos tenham acesso à instância 'db'
    from app.models.user import User
    from app.models.role import Role
    from app.models.permission import Permission
    from app.models.user_role import UserRole
    from app.models.role_permission import RolePermission
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app