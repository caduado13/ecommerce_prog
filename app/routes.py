from flask import render_template, request, url_for, flash, redirect, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.auth.forms import RegisterForm, LoginForm
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.auth.decorators import permission_required
from app.auth.forms import ProductForm, OrderStatusForm, UserForm

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


# --- PRODUTOS --------------------------------------------------

@main_bp.route('/produtos')
@login_required
@permission_required('view_products', redirect_endpoint='main.home')
def listar_produtos():
    produtos = Product.query.all()
    return render_template('produtos.html', produtos=produtos)


@main_bp.route('/produto/new', methods=['GET', 'POST'])
@login_required
@permission_required('crud_product', redirect_endpoint='main.vendedor_home')
def criar_produto():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data
        )
        db.session.add(p)
        db.session.commit()
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('main.vendedor_home'))
    return render_template('product_form.html', form=form, action='Criar')


@main_bp.route('/produto/<string:product_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('crud_product', redirect_endpoint='main.vendedor_home')
def editar_produto(product_id):
    p = Product.query.get_or_404(product_id)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        p.name = form.name.data
        p.price = form.price.data
        p.description = form.description.data
        db.session.commit()
        flash('Produto atualizado!', 'success')
        return redirect(url_for('main.vendedor_home'))
    return render_template('product_form.html', form=form, action='Editar')


@main_bp.route('/produto/<string:product_id>/delete', methods=['POST'])
@login_required
@permission_required('crud_product', redirect_endpoint='main.vendedor_home')
def deletar_produto(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash('Produto removido!', 'info')
    return redirect(url_for('main.vendedor_home'))


# --- COMPRA / PEDIDOS -----------------------------------------

@main_bp.route('/comprar/<string:product_id>', methods=['POST'])
@login_required
@permission_required('buy_products', redirect_endpoint='main.cliente_home')
def comprar_produto(product_id):
    # Cria um novo pedido para este usuário, com 1 unidade do produto
    pedido = Order(user_id=current_user.id)
    item = OrderItem(order=pedido, product_id=product_id, quantity=1)
    db.session.add_all([pedido, item])
    db.session.commit()
    flash('Compra realizada com sucesso!', 'success')
    return redirect(url_for('main.cliente_home'))


@main_bp.route('/orders')
@login_required
@permission_required('view_orders', redirect_endpoint='main.home')
def listar_pedidos():
    # Admin e vendedor veem todos, cliente vê só os seus
    if current_user.has_permission('manage_users'):
        orders = Order.query.order_by(Order.created_at.desc()).all()
    else:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)


@main_bp.route('/order/<int:order_id>/status', methods=['POST'])
@login_required
@permission_required('update_orders', redirect_endpoint='main.home')
def atualizar_status(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderStatusForm(request.form)
    if form.validate():
        order.status = form.status.data
        db.session.commit()
        flash('Status do pedido atualizado!', 'success')
    else:
        flash('Falha ao atualizar status.', 'danger')
    return redirect(url_for('main.listar_pedidos'))


# --- USUÁRIOS (ADMIN) -----------------------------------------

@main_bp.route('/admin/users')
@login_required
@permission_required('manage_users', redirect_endpoint='main.home')
def listar_usuarios():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@main_bp.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('manage_users', redirect_endpoint='main.home')
def editar_usuario(user_id):
    u = User.query.get_or_404(user_id)
    form = UserForm(obj=u)
    if form.validate_on_submit():
        u.name = form.name.data
        u.email = form.email.data
        # Exemplo: trocar papel
        u_roles = form.roles.data  # supondo um MultiSelectField de Role
        u.user_roles = []          # limpa roles atuais
        for role_id in u_roles:
            u.user_roles.append(UserRole(user_id=u.id, role_id=role_id))
        db.session.commit()
        flash('Usuário atualizado!', 'success')
        return redirect(url_for('main.listar_usuarios'))
    return render_template('admin/user_form.html', form=form, user=u)