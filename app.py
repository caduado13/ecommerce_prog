#from app import ecom_register
#from app import ecom_login
#
#menu_message = f'ECommerce, Bem vindo!\nDigite:\n[1] - Para logar na sua conta\n[2] - Registro de novo usuário\n[3] - Fechar o sistema!\nSua ação: '
#count = 0
#
#while True:
#    try:
#        menu_gui = int(input(menu_message))
#        if menu_gui == 1:
#            ecom_login.login_menu(count)
#            print(count)
#        elif menu_gui == 2:
#            ecom_register.register_user()
#        elif menu_gui == 3:
#            break
#    except:
#        input('[ERRO]Por favor digite um número!\nPressione enter para voltar ao sistema!')


from flask import Flask
from flask import render_template, request, url_for, redirect

from app import regex
from app import ecom_register
from app import utils

app = Flask(__name__)

@app.route("/register")
def register_render():
    return render_template('register.html')

@app.route("/register-form", methods = ['POST'])
def register_form():
    if request.method == 'POST':
        name = request.form['reg-name']
        email = request.form['reg-email']
        password = request.form['reg-password']
        cpf = request.form['reg-cpf']
        
        is_valid_email = regex.check_email(email)
        is_valid_password = regex.check_pass(password)
        is_valid_cpf = regex.check_cpf(cpf)

        if is_valid_email and is_valid_password and is_valid_cpf:
            ecom_register.register_user(name=name, password=password, email=email, cpf=cpf, db_path='./db/project.db')
            return redirect(url_for('login_render'))
    else:
        print('erro aqui')
        return "Este endpoint aceita apenas requisições POST."

@app.route("/login")
def login_render():
    return render_template('login.html')

@app.route("/login-form", methods = ['POST'])
def login_form():
    if request.method == 'POST':
        email = request.form['log-email']
        password = request.form['log-password']
        db_path = './db/project.db'
        login_result = utils.check_login(email, password, db_path)

        if login_result is True:
            return redirect(url_for("home_render"))
        else:
            return f'Login errado'
    else:
        return f'Erro de login'


@app.route("/home")
def home_render():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
