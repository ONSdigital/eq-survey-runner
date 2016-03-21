from flask import render_template
from flask_login import login_required, current_user
from .. import main_blueprint
from app.submitter.submitter import Submitter
from app.utilities.factory import factory
import logging
from app.main.views.root import _load_and_parse_schema
from app.main import errors


logger = logging.getLogger(__name__)


@main_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    logger.debug("Requesting thank you page")

    # load the response store
    response_store = factory.create("response-store")

    eq_id = current_user.get_eq_id()
    form_type = current_user.get_form_type()

    # load the schema
    schema = _load_and_parse_schema(eq_id, form_type)
    if not schema:
        return errors.page_not_found()

    submitter = Submitter()
    submitter.send_responses(current_user, schema, response_store.get_responses())
    return render_template('thank-you.html')
