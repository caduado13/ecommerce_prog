from app import create_app, db # Importa a função create_app e a instância db

app = create_app()

if __name__ == '__main__':
    # Você não precisa mais de db.create_all() aqui se já está em __init__.py
    # com app.app_context()
    app.run(debug=True)