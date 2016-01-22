import os

from flask import render_template, session
from .. import main

@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@main.route('/patterns/')
def patterns():
    files = []
    for (path, dirnames, filenames) in os.walk('app/templates/patterns/components/'):
        files.extend(name for name in filenames)

    return render_template('patterns/index.html', sections=files)
