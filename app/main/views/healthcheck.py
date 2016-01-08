from flask import render_template, session
from .. import main


@main.route('/healthcheck', methods=['GET'])
def HealthCheck():
    return "OK"
