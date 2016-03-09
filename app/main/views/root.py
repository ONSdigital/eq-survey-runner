from flask import render_template, json
from .. import main_blueprint


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/questionnaire/mci/', methods=['GET'])
def mci_survey():
    with main_blueprint.open_resource('../data/mci.json') as f:
        data = json.load(f)
    return render_template('questionnaire.html', questionnaire=data)


@main_blueprint.route('/cover-page', methods=['GET'])
def cover_page():
    return render_template('cover-page.html')
