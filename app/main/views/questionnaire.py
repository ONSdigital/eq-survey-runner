import logging

from flask import request
from flask_login import login_required, current_user
from flask import redirect
from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.submitter.submission_failed import SubmissionFailedException
from .. import main_blueprint
from app.schema.questionnaire import QuestionnaireException
from app.main.errors import page_not_found, internal_server_error, service_unavailable
from flask_themes2 import render_theme_template
from app.metadata.metadata_store import MetaDataStore
from flask_wtf import Form
from wtforms import SelectField, IntegerField, DateField, SelectMultipleField, TextAreaField
from wtforms.widgets import TextArea, TextInput, RadioInput, CheckboxInput, ListWidget
from wtforms import validators

logger = logging.getLogger(__name__)


def generate_form(block):
    class QuestionnaireForm(Form):
        pass

    for section in block.sections:
        for question in section.questions:
            for answer in question.answers:
                name = answer.label if answer.label else question.title
                setattr(QuestionnaireForm, answer.id, get_field(answer, name))

    form = QuestionnaireForm()
    print(form)
    return form


def get_field(answer, label):
    print(answer.type)
    if answer.type == 'Radio':
        field = SelectField(label=label, description=answer.guidance, choices=build_choices(answer.options), widget=ListWidget(), option_widget=RadioInput())
    if answer.type == 'Checkbox':
        field = SelectMultipleField(label=label, description=answer.guidance, choices=build_choices(answer.options), widget=ListWidget(), option_widget=CheckboxInput())
    if answer.type == 'Date':
        field = DateField(label=label, description=answer.guidance, widget=TextInput(), validators=[validators.optional()])
    if answer.type == 'Currency' or answer.type == 'PositiveInteger' or answer.type == 'Integer':
        field = IntegerField(label=label, description=answer.guidance, widget=TextInput())
    if answer.type == 'Textarea':
        field = TextAreaField(label=label, description=answer.guidance, widget=TextArea())

    print(field)

    return field


def build_choices(options):
    choices = []
    for option in options:
        choices.append((option['label'], option['value']))
    return choices


@main_blueprint.route('/questionnaire/<eq_id>/<collection_id>/<location>', methods=["GET", "POST"])
@login_required
def survey(eq_id, collection_id, location):

    logger.debug("Requesting location : /questionnaire/%s/%s/%s", eq_id, collection_id, location)
    try:
        questionnaire_manager = create_questionnaire_manager()

        # Redirect to thank you page if the questionnaire has already been submitted
        if questionnaire_manager.submitted and location != 'thank-you':
            return do_redirect(eq_id, collection_id, 'thank-you')

        # redirect to the first block if the change your answers link is clicked
        if location == 'first':
            questionnaire_manager.go_to(location)
            return do_redirect(eq_id, collection_id, questionnaire_manager.get_current_location())

        block_id = questionnaire_manager.get_current_location()
        schema = questionnaire_manager._schema
        if schema.item_exists(location):
            form = generate_form(schema.get_item_by_id(block_id))
        else:
            form = Form()

        # Process the POST request
        if request.method == "POST":
            # currently only supporting WTforms on the block pages not intro, or summary
            if schema.item_exists(location):
                form.validate_on_submit()
            return do_post(collection_id, eq_id, location, questionnaire_manager, form.data)
        else:
            return do_get(questionnaire_manager, location, schema, form)

    except QuestionnaireException as e:
        return page_not_found(e)
    except SubmissionFailedException as e:
        # Rabbit MQ connection issue
        return service_unavailable(e)
    except Exception as e:
        return internal_server_error(e)


def do_redirect(eq_id, collection_id,  location):
    return redirect('/questionnaire/' + eq_id + '/' + collection_id + '/' + location)


def do_get(questionnaire_manager, location, schema, form):
    questionnaire_manager.go_to(location)
    context = questionnaire_manager.get_rendering_context()
    template = questionnaire_manager.get_rendering_template()

    # the special case where a get request modifies state
    if location == 'thank-you':
        questionnaire_manager.delete_user_data()
    try:
        theme = context['meta']['survey']['theme']
        logger.info("Theme selected: {} ".format(theme))
    except KeyError:
        logger.info("No theme set ")
        theme = None

    if schema.item_exists(location):
        return render_theme_template(theme=theme, template_name="wtforms_questionnaire.html", form=form)
    else:
        return render_theme_template(theme, template, meta=context['meta'], content=context['content'], navigation=context['navigation'])


def do_post(collection_id, eq_id, location, questionnaire_manager, data):
    print(data)
    logger.debug("POST request question - current location %s", location)
    questionnaire_manager.process_incoming_answers(location, data, 'save_continue')
    next_location = questionnaire_manager.get_current_location()
    metadata = MetaDataStore.get_instance(current_user)
    logger.info("Redirecting user to next location %s with tx_id=%s", next_location, metadata.tx_id)
    return redirect('/questionnaire/' + eq_id + '/' + collection_id + '/' + next_location)
