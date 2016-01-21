from flask import render_template, session
from .. import main


@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main.route('/patterns/')
def hello():
    return render_template('patterns/index.html')
