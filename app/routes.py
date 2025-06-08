from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.auth.forms import RegisterForm, LoginForm
from app.models.product import Product

main_bp = Blueprint('main', __name__, template_folder='templates')
auth_bp = Blueprint('auth', __name__, template_folder='templates')

def redirect_user_home():
    roles = [ur.role.name for ur in current_user.user_roles]

    if 'admin' in roles:
        return redirect(url_for('main.admin_home'))
    elif 'vendedor' in roles:
        return redirect(url_for('main.vendedor_home'))
    elif 'cliente' in roles:
        return redirect(url_for('main.cliente_home'))
    else:
        flash("Sem perfil de acesso definido.", "warning")
        return redirect(url_for('main.home'))

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
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
            print(cliente_role)
            if cliente_role:
                UserRole.assign_role(user_id=user.id, role_id=cliente_role.id)
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
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_user_home()
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user=user)
            flash('Login bem-sucedido!')
            return redirect_user_home()
        else:
            flash('Login falhou, tente novamente!')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required # Garante que apenas usuários logados podem acessar esta rota
def logout():
    logout_user() # Função do Flask-Login para deslogar o usuário
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.home'))

@main_bp.route('/admin/home')
@login_required
def admin_home():
    if not current_user.has_permission('view_admin_dashboard'):
        flash("Acesso negado.", "danger")
        return redirect(url_for('main.home'))
    return render_template('home.html', role='admin')


@main_bp.route('/vendedor/home')
@login_required
def vendedor_home():
    if not current_user.has_permission('crud_product'):
        flash("Acesso negado.", "danger")
        return redirect(url_for('main.home'))
    return render_template('home.html', role='vendedor')


@main_bp.route('/cliente/home')
@login_required
def cliente_home():
    products = Product.query.all()
    if not current_user.has_permission('view_products'):
        flash("Acesso negado.", "danger")
        return redirect(url_for('main.home'))
    return render_template('home.html', role='cliente',  products=products)