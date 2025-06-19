from functools import wraps
from flask import abort, request, redirect, url_for
from flask_login import current_user
from app import login_manager # Assuming login_manager is accessible from app package

def roles_required(*roles_to_check):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                # If login_manager.login_view is set, Flask-Login handles this redirect automatically
                # or we can be explicit.
                # For @login_required, it redirects to login_manager.login_view
                # Here, we ensure similar behavior if user is not authenticated at all.
                return redirect(url_for(login_manager.login_view, next=request.url))

            if current_user.role not in roles_to_check:
                abort(403) # Forbidden
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
