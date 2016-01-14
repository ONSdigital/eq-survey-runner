from flask import render_template
from app.main import main
import traceback


@main.app_errorhandler(400)
def page_not_found(e):
    print(e)
    return _render_error_page(500)


@main.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return _render_error_page(404)


@main.app_errorhandler(500)
def exception(e):
    traceback.print_exc()
    return _render_error_page(500)


@main.app_errorhandler(503)
def service_unavailable(e):
    print(e)
    return _render_error_page(503)


def _render_error_page(status_code):
    template_map = {
        404: "errors/404.html",
        500: "errors/500.html",
        503: "errors/500.html",
    }
    if status_code not in template_map:
        status_code = 500
    return render_template(template_map[status_code]), status_code
