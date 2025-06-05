from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.auth.forms import RegisterForm, LoginForm

from app import regex
from app import utils

main_bp = Blueprint('main', __name__, template_folder='templates')
auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_autenticated:
        return redirect(url_for('main.home'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.create_user(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                cpf=form.cpf.data
            )
            cliente_role = Role.query.filter_by(name='cliente').first()
            if cliente_role:
                UserRole.assign_role(user=user.id, role=cliente_role.id)
            else:
                flash('Erro: Papel "cliente" não encontrado no banco de dados. Contate o administrador.', 'danger')
                db.session.rollback()
                return render_template('register.html', title='Register', form=form)
            
            flash('Sua conta foi criada com sucesso')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback() # Em caso de qualquer erro, desfaça as alterações no banco
            flash(f'Ocorreu um erro ao registrar sua conta: {e}', 'danger')
            print(f"Erro de registro: {e}") # Para depuração no console
    return render_template('register.html', title='Registrar', form=form)

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_autenticate:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            next_page = request.args.get('next') # Pega a URL de onde o usuário veio, se houver
            flash('Login bem sucedido!')
            return redirect(next_page or url_for)
        else:
            flash('Login falhou, tente novamente!')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required # Garante que apenas usuários logados podem acessar esta rota
def logout():
    logout_user() # Função do Flask-Login para deslogar o usuário
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.home'))

@main_bp.route("/register") #Template da página de registro
def register_render():
    return render_template('register.html')

@main_bp.route("/register-form", methods = ['POST']) #Rota para checar form (register)
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
            utils.register_user(name=name, password=password, email=email, cpf=cpf, db_path='./db/project.db')
            return redirect(url_for('main.login_render'))
    else:
        print('erro aqui')
        return "Este endpoint aceita apenas requisições POST."

@main_bp.route("/login") #Template da página de login
def login_render():
    return render_template('login.html')

@main_bp.route("/login-form", methods = ['POST']) #Rota para checar form (login)
def login_form():
    if request.method == 'POST':
        email = request.form['log-email']
        password = request.form['log-password']
        db_path = './db/project.db'
        login_result = utils.check_login(email, password, db_path)

        if login_result is True:
            return redirect(url_for("main.home_render"))
        else:
            return f'Login errado'
    else:
        return f'Erro de login'


@main_bp.route("/home") #Template da página principal
def home_render():
    return render_template("home.html")
