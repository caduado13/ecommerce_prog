# app/utils.py
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def permission_required(permission_name, redirect_endpoint='main.home', message="Acesso negado"):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(permission_name):
                flash(message, 'danger')
                return redirect(url_for(redirect_endpoint))
            return f(*args, **kwargs)
        return wrapped
    return decorator