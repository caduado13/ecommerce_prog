from app import db, bcrypt
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    email = db.Column(db.String(128), unique = True , nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    cpf = db.Column(db.String(11), unique = True, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    user_roles = db.relationship('UserRole', back_populates='user', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email}>' # Ex: <User meu@email.com>

    def set_password(self, password):
        # Gera o hash da senha e decodifica para string (UTF-8)
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        # Compara a senha fornecida com o hash armazenado
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_email(cls, email):
        #Procura um email e trás o primeiro
        return cls.query.filter_by(email=email).first()
    @classmethod
    def create_user(cls, name, email, password, cpf):
        # Cria uma nova instância de User
        user = cls(name=name, email=email, cpf=cpf) 
        user.set_password(password) 
        db.session.add(user)
        db.session.commit()
        
        return user
    
