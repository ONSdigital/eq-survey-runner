import os
import markdown
import yaml

from flask import render_template, session
from .. import main

@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@main.route('/patterns/')
def patterns():
    sections = []
    for root, dirs, files in os.walk('app/templates/patterns/components/'):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), 'r') as f:
                  front_matter, content = list(yaml.load_all(f))[:2]
                  sections.append({
                    "title": front_matter['title'],
                    "content": markdown.markdown(content)
                  })

    return render_template('patterns/index.html', sections=sections)
