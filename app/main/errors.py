from flask import render_template
from app.main import main
import logging


@main.app_errorhandler(400)
def bad_request(e):
    logging.error(e)
    return _render_error_page(500)


@main.app_errorhandler(401)
def unauthorized(e):
    logging.error(e)
    return _render_error_page(401)


@main.app_errorhandler(403)
def forbidden(e):
    logging.error(e)
    return _render_error_page(403)


@main.app_errorhandler(404)
def page_not_found(e):
    logging.error(e)
    return _render_error_page(404)


@main.app_errorhandler(500)
def exception(e):
    logging.error(e)
    return _render_error_page(500)


@main.app_errorhandler(503)
def service_unavailable(e):
    logging.error(e)
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
