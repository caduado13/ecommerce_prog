from app import db
from datetime import datetime

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    user = db.relationship('User', back_populates = 'user_roles')
    role = db.relationship('Role', back_populates = 'user_roles')

    def __repr__(self):
        return f'<UserRole UserID:{self.user_id} RoleID:{self.role_id}>'

    @classmethod
    def assign_role(cls, user_id, role_id):
        exististing_associoation = cls.query.filter_by(user_id=user_id, role_id=role_id).first()
        if exististing_associoation:
            return
        association = cls(user_id=user_id, role_id=role_id)
        db.session.add(association)
        db.session.commit()
        return association
    
    @classmethod
    def remove_role(cls, user_id, role_id):
        association = cls.query.filter_by(user_id=user_id, role_id=role_id).first()
        if association:
            db.session.delete(association)
            db.session.commit()
            return True
        return False