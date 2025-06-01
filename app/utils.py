import sqlite3
import bcrypt
import traceback
import sys


def check_login(email, password, db_path):
    try:
        with sqlite3.connect(db_path) as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT email, senha FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if user:
                email_stored, password_stored = user
                if bcrypt.checkpw(password.encode('utf-8'), password_stored):
                    return True #Senha correta!
                else:
                    return False #Senha incorreta!
            else:
                return False #Usuário não encontrado
                
    except Exception as e:
        # Exibe o erro completo no terminal
        print("\n--- DEBUG (ERRO INTERNO) ---", file=sys.stderr)
        traceback.print_exc()  # Mostra o stack trace completo
        print("----------------------------", file=sys.stderr)
        #Erro amigável ao usuário
        

