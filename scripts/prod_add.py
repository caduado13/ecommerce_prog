import os
import sys

# Adiciona o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.product import Product

# Cria e ativa o app context
app = create_app()
with app.app_context():
    # Cria as tabelas no banco se ainda não existirem
    db.create_all()

    # Adiciona produtos de exemplo
    product1 = Product(name="Camiseta Branca", price=49.90)
    product2 = Product(name="Calça Jeans", price=129.99)
    db.session.add_all([product1, product2])
    db.session.commit()

    print("Produtos adicionados com sucesso!")