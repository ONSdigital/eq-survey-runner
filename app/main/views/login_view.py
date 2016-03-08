from flask.views import MethodView
from flask import request, redirect
from app.authentication.authenticator import Authenticator
from app.authentication.session_management import session_manager
from app.authentication.no_token_exception import NoTokenException
from app.authentication.invalid_token_exception import InvalidTokenException
from app.main import errors
import logging


class LoginView(MethodView):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get(self):
        authenticator = Authenticator()
        self.logger.debug("Attempting token authentication")
        try:
            token = authenticator.jwt_login(request)
            self.logger.debug("Token authenticated - linking to session")
            session_manager.add_token(token)
            return redirect("/questionnaire/1")
        except NoTokenException as e:
            self.logger.warning("Unable to authenticate user", e)
            return errors.unauthorized(e)
        except InvalidTokenException as e:
            self.logger.warning("Invalid Token provided", e)
            return errors.forbidden(e)
