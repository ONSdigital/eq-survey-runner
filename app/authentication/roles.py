from functools import wraps
from flask_login import current_user
from werkzeug.exceptions import Forbidden
from app.globals import get_metadata_async


def role_required(role):
    """
    If you decorate a view with this, it will ensure that the current user has
    the specified role before calling the actual view. (If they are
    not, it raises a Forbidden exception) For
    example::

        @app.route('/dump')
        @login_required
        @role_required('dumper')
        def dump():
            pass

    This decorator should be used after the flask_login.login_required
    decorator to ensure that the user is logged in before their role is checked.

    :param role: The role required by the function being decorated
    """
    def role_required_decorator(func):
        @wraps(func)
        async def role_required_wrapper(*args, **kwargs):
            metadata = await get_metadata_async(current_user)
            roles = (metadata.get('roles', []) or []) if metadata else []
            if current_user.is_authenticated and role in roles:
                return await func(*args, **kwargs)
            raise Forbidden
        return role_required_wrapper
    return role_required_decorator
