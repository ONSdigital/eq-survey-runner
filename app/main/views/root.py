import os
import markdown

from flask import render_template, session
from .. import main
import markdown

@main.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@main.route('/patterns/')
def patterns():
    sections = []
    for root, dirs, files in os.walk('app/templates/patterns/components/'):
        for file in files:
            if file.endswith(".md"):
                f = open(os.path.join(root, file), 'r')
                sections.append( {
                  "title": file.replace(".md", " "),
                  "content": markdown.markdown( f.read() )
                })

    return render_template('patterns/index.html', sections=sections)
