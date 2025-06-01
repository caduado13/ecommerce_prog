#user schema
#name | senha | cpf | email | id
import sqlite3
import bcrypt
import traceback
import sys

def register_user(password, name, cpf, email, db_path, id = 1,):
    with sqlite3.connect(db_path) as connect:
        cursor = connect.cursor()
        try:
            hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
            cursor.execute('INSERT INTO users (name, senha, cpf, email, id) VALUES(?,?,?,?,?)', (name, hashed_pass, cpf, email, id))
            connect.commit()
        except Exception as e:
            # Exibe o erro completo no terminal
            print("\n--- DEBUG (ERRO INTERNO) ---", file=sys.stderr)
            traceback.print_exc()  # Mostra o stack trace completo
            print("----------------------------", file=sys.stderr)
            #Erro amigável ao usuário