import os
import markdown
import yaml
from flask import render_template, render_template_string, session
from .. import main
from application import application

@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@main.route('/patterns/')
def patterns():
    sections = []
    for root, dirs, files in os.walk('app/templates/patterns/components/'):
        for file in files:
            if file.endswith(".html"):
              with open(os.path.join(root, file), 'r') as f:
                sections.append({
                  "title": file.replace('.html', ''),
                  "content": render_template_string(f.read())
                })

    return render_template('patterns/index.html', sections=sections)
