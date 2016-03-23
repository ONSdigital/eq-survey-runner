from flask import render_template
from app.main import main_blueprint
import logging

logger = logging.getLogger(__name__)


@main_blueprint.app_errorhandler(400)
def bad_request(error=None):
    if error:
        logger.error(error)
    return _render_error_page(500)


@main_blueprint.app_errorhandler(401)
def unauthorized(error=None):
    if error:
        logger.error(error)
    return _render_error_page(401)


@main_blueprint.app_errorhandler(403)
def forbidden(error=None):
    if error:
        logger.error(error)
    return _render_error_page(403)


@main_blueprint.app_errorhandler(404)
def page_not_found(error=None):
    if error:
        logger.error(error)
    return _render_error_page(404)


@main_blueprint.app_errorhandler(500)
def internal_server_error(error=None):
    if error:
        logger.error(error)
    return _render_error_page(500)


@main_blueprint.app_errorhandler(503)
def service_unavailable(error=None):
    if error:
        logger.error(error)
    return _render_error_page(503)


def _render_error_page(status_code):
    template_map = {
        401: "errors/401.html",
        403: "errors/403.html",
        404: "errors/404.html",
        500: "errors/500.html",
        503: "errors/500.html",
    }
    if status_code not in template_map:
        status_code = 500
    return render_template(template_map[status_code]), status_code
