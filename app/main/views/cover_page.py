from flask import render_template
from flask_login import login_required
from .. import main_blueprint
import logging


logger = logging.getLogger(__name__)


@main_blueprint.route('/cover-page', methods=['GET', 'POST'])
@login_required
def cover_page():
    logger.debug("Requesting cover page")
    return render_template('cover-page.html')
