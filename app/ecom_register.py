#user schema
#name | senha | cpf | email | id
import sqlite3
import bcrypt
import traceback
import sys
from app import regex

connect = sqlite3.connect('./db/project.db')
cursor = connect.cursor() 

def register_user():
    try:
        name = input('Digite seu nome completo: ')
        #Funções regex aplicadas
        password = input('Digite sua senha: ') 
        while not regex.check_pass(password):
            print('Senha precisa conter\nUm simbolo especial\nUma letra maiúscula\nUm número\nPelo menos 8 caracteres')
            password = input('Dgite novamente: ')

        cpf = input('Digite seu cpf: ')
        while not regex.check_cpf(cpf):
            print('Cpf incorreto')
            cpf = input('Dgite novamente: ')

        email = input('Digite seu e-mail: ')
        while not regex.check_email(email):
            print('Email inválido')
            email = input('Dgite novamente: ')

        id = int(input('Digite [1] se deseja se cadastrar como cliente\nDigite [2] para se cadastrar como vendedor\nR: '))
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

        cursor.execute('INSERT INTO users (name, senha, cpf, email, id) VALUES(?,?,?,?,?)', (name, hashed_pass, cpf, email, id))
        connect.commit()
    except Exception as e:
        # Exibe o erro completo no terminal
        print("\n--- DEBUG (ERRO INTERNO) ---", file=sys.stderr)
        traceback.print_exc()  # Mostra o stack trace completo
        print("----------------------------", file=sys.stderr)
        #Erro amigável ao usuário
        input('[ERRO]Por favor confira seus dados e tente novamente. \nPressione enter para voltar ao sistema!')
    finally:
        connect.close()
