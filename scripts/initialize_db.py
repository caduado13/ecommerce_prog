import os
import sys

# Pega o diretório do script (scripts/)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para chegar ao diretório raiz do projeto (ecommerce-flask/)
project_root = os.path.join(script_dir, '..')
# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, project_root)
# Ajuste a importação de 'app' para que ela encontre a função create_app
# e as instâncias db, bcrypt, etc. que estão em 'app/__init__.py'
from app import create_app, db, bcrypt

# Importe os modelos diretamente da pasta 'app.models'
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.models.order import Order, OrderItem 


def initialize_database():
    # A função create_app já cuida da configuração do caminho do DB
    app = create_app()

    with app.app_context():
        print("Initializing database...")
        db.create_all()

        # --- Initial Population of Roles ---
        if not Role.query.filter_by(name='admin').first():
            db.session.add(Role(name='admin'))
        if not Role.query.filter_by(name='vendedor').first():
            db.session.add(Role(name='vendedor'))
        if not Role.query.filter_by(name='cliente').first():
            db.session.add(Role(name='cliente'))
        db.session.commit()

        # --- Initial Population of Permissions ---
        permissions_to_add = [
            ('crud_product', 'Permite criar, ler, atualizar e deletar produtos.'),
            ('view_products', 'Permite visualizar a lista de produtos.'),
            ('buy_products', 'Permite comprar produtos.'),
            ('view_orders', 'Permite visualizar pedidos.'),
            ('update_orders', 'Permite atualizar o status de pedidos.'),
            ('manage_users', 'Permite gerenciar usuários (criação, edição, exclusão).')
        ]
        for permission, description in permissions_to_add:
            if not Permission.query.filter_by(name=permission).first():
                db.session.add(Permission(name=permission, description=description))
        db.session.commit()

        # --- Initial Admin User (Optional) ---
        if not User.query.filter_by(email='admin@gmail.com').first():
            print("Creating initial admin user...")
            # Use bcrypt para hash da senha do admin
            hashed_password = bcrypt.generate_password_hash('adminpassword').decode('utf-8')
            admin_user = User(
                name='Admin',
                email='admin@gmail.com',
                password_hash=hashed_password,
                cpf='00000000000'
            )
            db.session.add(admin_user)
            db.session.commit() # Commit para ter o ID do admin_user

            admin_role = Role.query.filter_by(name='admin').first()
            if admin_role:
                # Use o método assign_role do modelo UserRole
                UserRole.assign_role(admin_user.id, admin_role.id)
                db.session.commit() # Commit para a associação de papel
            print("Admin user created!")

        # --- Assigning Permissions to Roles ---
        admin_role = Role.query.filter_by(name='admin').first()
        vendedor_role = Role.query.filter_by(name='vendedor').first()
        cliente_role = Role.query.filter_by(name='cliente').first()

        crud_product_perm = Permission.query.filter_by(name='crud_product').first()
        view_products_perm = Permission.query.filter_by(name='view_products').first()
        buy_products_perm = Permission.query.filter_by(name='buy_products').first()
        view_orders_perm = Permission.query.filter_by(name='view_orders').first()
        update_orders_perm = Permission.query.filter_by(name='update_orders').first()
        manage_users_perm = Permission.query.filter_by(name='manage_users').first()

        def assign_if_not_exists(role_obj, perm_obj):
            if role_obj and perm_obj:
                exists = RolePermission.query.filter_by(role_id=role_obj.id, permission_id=perm_obj.id).first()
                if not exists:
                    db.session.add(RolePermission(role=role_obj, permission=perm_obj))

        # Admin Permissions
        assign_if_not_exists(admin_role, crud_product_perm)
        assign_if_not_exists(admin_role, view_products_perm)
        assign_if_not_exists(admin_role, view_orders_perm)
        assign_if_not_exists(admin_role, update_orders_perm)
        assign_if_not_exists(admin_role, manage_users_perm)

        # Vendedor Permissions
        assign_if_not_exists(vendedor_role, crud_product_perm)
        assign_if_not_exists(vendedor_role, view_products_perm)
        assign_if_not_exists(vendedor_role, view_orders_perm)
        assign_if_not_exists(vendedor_role, update_orders_perm)

        # Cliente Permissions
        assign_if_not_exists(cliente_role, view_products_perm)
        assign_if_not_exists(cliente_role, buy_products_perm)
        assign_if_not_exists(cliente_role, view_orders_perm)

        db.session.commit()
        print("Database initialization complete!")

if __name__ == '__main__':
    initialize_database()