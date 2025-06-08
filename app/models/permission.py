from app import db

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    description = db.Column(db.String(128), nullable = False)
    role_permissions = db.relationship('RolePermission', back_populates='permission', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Permission {self.name}'
    
    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    