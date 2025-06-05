from app import db
from datetime import datetime

class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    role = db.relationship('Role', back_populates='role_permissions')
    permission = db.relationship('Permission', back_populates='role_permissions')

    def __repr__(self):
        return f'<RolePermission RoleID:{self.role_id} PermissionID:{self.permission_id}>'
    
    # Métodos de Classe para atribuição e remoção
    @classmethod
    def assign_permission(cls, role, permission):
        existing_association = cls.query.filter_by(role_id=role.id, permission_id=permission.id).first()
        if existing_association:
            return existing_association
        
        association = cls(role=role, permission=permission)
        db.session.add(association)
        db.session.commit()
        return association

    @classmethod
    def remove_permission(cls, role, permission):
        association = cls.query.filter_by(role_id=role.id, permission_id=permission.id).first()
        if association:
            db.session.delete(association)
            db.session.commit()
            return True
        return False