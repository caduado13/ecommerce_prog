import sqlite3
import bcrypt
import traceback
import sys


def check_login(email, password, flag= False):
    try:
        with sqlite3.connect("./db/project.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email, senha FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            while True:
                if user:
                    email_stored, password_stored = user
                    if bcrypt.checkpw(password.encode('utf-8'), password_stored):
                        print("Conectado!")  
                        flag = True
                        break
                    else:
                        print("Senha incorreta!")
                        password = input('Tente novamente: ')
                else:
                    print("Usuário não encontrado!")
                    break
    except Exception as e:
        # Exibe o erro completo no terminal
        print("\n--- DEBUG (ERRO INTERNO) ---", file=sys.stderr)
        traceback.print_exc()  # Mostra o stack trace completo
        print("----------------------------", file=sys.stderr)
        #Erro amigável ao usuário
        input('[ERRO]Por favor confira seus dados e tente novamente. \nPressione enter para voltar ao sistema!')

    return flag


