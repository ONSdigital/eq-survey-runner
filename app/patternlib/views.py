from flask import render_template,  redirect, json
from . import patternlib_blueprint
import os


@patternlib_blueprint.route('/pattern-library/')
def index():
    return redirect("/pattern-library/styleguide/typography", code=301)


@patternlib_blueprint.route('/pattern-library/<section>/<pattern>', methods=['GET', 'POST'])
def patterns(section='styleguide', pattern='index'):
    trimmed = {}

    def trim(str):
        trimmed_str = str.split('-', 1)[-1:][0]
        trimmed[trimmed_str] = str
        return trimmed_str

    def untrim(str):
        return trimmed[str]

    def make_section(sectionDir, dir, dirName):
        section = {
          'sections': [],
          'title': dirName
        }
        for root, dirs, files in os.walk(sectionDir):
            for file in files:
                if file.endswith('.html'):
                    # The following line causes problems with flake8, so we use `# NOQA` to ignore it
                    with open(os.path.join(root, file), 'r') as f:           # NOQA
                        title = trim(file.replace('.html', ''))
                        url = '/pattern-library/' + dirName + "/" + trim(file.replace('.html', ''))
                        section['sections'].append({
                            'url': url,
                            'title': title.replace('-', ' '),
                            'current': True if (url == pattern) else False
                        })
        return section

    with patternlib_blueprint.open_resource('patterns.json') as f:
        data = json.load(f)

    sections = {}
    pattern_title = pattern.split('-', 1)[-1:][0]

    for root, dirs, files in os.walk(patternlib_blueprint.root_path + '/templates/'):
        for dir in dirs:
            dirName = trim(dir)
            sections[dirName] = make_section(os.path.join(root, dir), dir, dirName)

    pattern_include = untrim(section) + '/' + untrim(pattern) + '.html'
    return render_template('patterns.html', sections=sections, pattern_include=pattern_include, title=pattern_title, data=data)
