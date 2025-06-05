from app import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    user_roles = db.relationship('UserRole', back_populates='role', lazy='dynamic', cascade="all, delete-orphan")
    role_permissions = db.relationship('RolePermission', back_populates='role', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Role {self.name}>'
    
    @classmethod
    def create_role(cls, name):
        return cls.query.filter_by(name = name).first()
