import logging

from app.authentication.session_storage import session_storage
from app.data_model.answer_store import Answer

from app.globals import get_answer_store, get_completed_blocks, get_metadata, get_questionnaire_store
from app.helpers.forms import build_relationship_choices, HouseHoldCompositionForm, Struct, generate_form, generate_relationship_form
from app.helpers.schema_helper import SchemaHelper
from app.questionnaire.location import Location
from app.questionnaire.navigation import Navigation
from app.questionnaire.path_finder import PathFinder
from app.submitter.converter import convert_answers
from app.submitter.submitter import SubmitterFactory
from app.templating.introduction_context import get_introduction_context
from app.templating.metadata_context import build_metadata_context
from app.templating.schema_context import build_schema_context
from app.templating.summary_context import build_summary_rendering_context
from app.templating.template_renderer import renderer
from app.utilities.schema import get_schema
from app.views.errors import MultipleSurveyError

from flask import redirect
from flask import request
from flask import Blueprint
from flask import g
from flask import url_for

from flask_login import current_user
from flask_login import login_required

from flask_themes2 import render_theme_template

from werkzeug.exceptions import NotFound

logger = logging.getLogger(__name__)


questionnaire_blueprint = Blueprint(name='questionnaire',
                                    import_name=__name__,
                                    url_prefix='/questionnaire/<eq_id>/<form_type>/<collection_id>/')


@questionnaire_blueprint.before_request
@login_required
def check_survey_state():
    g.schema_json, g.schema = get_schema(get_metadata(current_user))
    values = request.view_args

    _check_same_survey(values['eq_id'], values['form_type'], values['collection_id'])


@questionnaire_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True

    return response


@questionnaire_blueprint.after_request
def save_questionnaire_store(response):
    if not current_user.is_anonymous:
        questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

        if questionnaire_store.has_changed():
            questionnaire_store.add_or_update()

    return response


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["GET"])
@login_required
def get_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    # Filter answers down to those we may need to render
    answer_store = get_answer_store(current_user)

    current_location = Location(group_id, group_instance, block_id)

    block = SchemaHelper.get_block_for_location(g.schema_json, current_location)

    logger.info(answer_store.answers)

    if block_id == 'household-composition':
        household = next((a['value'] for a in answer_store.answers if a['answer_id'] == 'household'), None)
        form_data = {'household': household}

        data_class = Struct(**form_data)
        form = HouseHoldCompositionForm(csrf_enabled=False, obj=data_class)
        content = {'form': form, 'block': block}
    elif block_id == 'relationships':
        relationships = next((a['value'] for a in answer_store.answers if a['answer_id'] == 'who-is-related'), None)
        choices = build_relationship_choices(answer_store, group_instance)
        form = generate_relationship_form(block, len(choices), {'who-is-related': relationships})

        content = {
            'form': form,
            'block': block,
            'relation_instances': choices
        }
    else:
        answers = answer_store.map(
            group_id=group_id,
            group_instance=group_instance,
            block_id=block_id
        )

        form = generate_form(block, answers)

        content = {'form': form, 'block': block}
    template = block['type'] if block and 'type' in block and block['type'] else 'questionnaire'

    return _render_template(content, current_location=current_location, template=template)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/<block_id>', methods=["POST"])
@login_required
def post_block(eq_id, form_type, collection_id, group_id, group_instance, block_id):
    path_finder = PathFinder(g.schema_json, get_answer_store(current_user), get_metadata(current_user))

    current_location = Location(group_id, group_instance, block_id)

    valid_location = current_location in path_finder.get_routing_path(group_id, group_instance)

    block = SchemaHelper.get_block_for_location(g.schema_json, current_location)

    if block_id == 'relationships':
        choices = build_relationship_choices(get_answer_store(current_user), group_instance)
        form = generate_relationship_form(block, len(choices), request.form)
    else:
        form = generate_form(block, request.form.to_dict())

    valid_data = form.validate()

    if not valid_location or not valid_data:
        return _render_template({'form': form, 'block': block}, block_id=block_id, template='questionnaire')
    else:
        update_questionnaire_store(current_location, form.data)

    next_location = path_finder.get_next_location(current_location=current_location)
    metadata = get_metadata(current_user)

    if next_location is None:
        raise NotFound

    if next_location.block_id == 'confirmation':
        return redirect_to_confirmation(eq_id, form_type, collection_id)

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('<group_id>/0/household-composition', methods=["POST"])
@login_required
def post_household_composition(eq_id, form_type, collection_id, group_id):
    path_finder = PathFinder(g.schema_json, get_metadata(current_user), get_answer_store(current_user))
    answer_store = get_answer_store(current_user)

    form = HouseHoldCompositionForm(csrf_enabled=False, obj=request.form)
    current_location = Location(group_id, 0, 'household-composition')
    block = SchemaHelper.get_block_for_location(g.schema_json, current_location)

    if 'action[save_continue]' in request.form:
        _remove_repeating_on_household_answers(answer_store, group_id)

    if 'action[add_answer]' in request.form:
        form.household.append_entry()
    elif 'action[remove_answer]' in request.form:
        index_to_remove = int(request.form.get('action[remove_answer]'))

        form.remove_person(index_to_remove)

    if not form.validate() or 'action[add_answer]' in request.form or 'action[remove_answer]' in request.form:
        return _render_template({
            'form': form,
            'block': block,
        }, current_location=current_location, template='questionnaire')

    update_questionnaire_store(current_location, form.data)

    next_location = path_finder.get_next_location(current_location=current_location)

    metadata = get_metadata(current_user)

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('introduction', methods=["GET"])
@login_required
def get_introduction(eq_id, form_type, collection_id):
    return _render_template(get_introduction_context(g.schema_json), block_id='introduction')


@questionnaire_blueprint.route('<block_id>', methods=["POST"])
@login_required
def post_interstitial(eq_id, form_type, collection_id, block_id):
    path_finder = PathFinder(g.schema_json, get_answer_store(current_user), get_metadata(current_user))

    current_location = Location(SchemaHelper.get_first_group_id(g.schema_json), 0, block_id)

    valid_location = current_location in path_finder.get_location_path()
    update_questionnaire_store(current_location, request.form.to_dict())

    # Don't care if data is valid because there isn't any for interstitial
    if not valid_location:
        block = SchemaHelper.get_block_for_location(g.schema_json, current_location)

        return _render_template({"block": block}, current_location=current_location, template='questionnaire')

    next_location = path_finder.get_next_location(current_location=current_location)

    metadata = get_metadata(current_user)

    if next_location is None:
        raise NotFound

    logger.info("Redirecting user to next location %s with tx_id=%s", str(next_location), metadata["tx_id"])

    return redirect(next_location.url(metadata))


@questionnaire_blueprint.route('summary', methods=["GET"])
@login_required
def get_summary(eq_id, form_type, collection_id):

    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, get_metadata(current_user))
    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user))
    metadata = get_metadata(current_user)

    if latest_location.block_id is 'summary':
        schema_context = build_schema_context(metadata, g.schema.aliases, answer_store)
        rendered_schema_json = renderer.render(g.schema_json, **schema_context)
        summary_context = build_summary_rendering_context(rendered_schema_json, answer_store, metadata)
        return _render_template(summary_context, current_location=latest_location)

    return redirect(latest_location.url(metadata))


@questionnaire_blueprint.route('confirmation', methods=["GET"])
@login_required
def get_confirmation(eq_id, form_type, collection_id):
    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, get_metadata(current_user))

    latest_location = path_finder.get_latest_location(get_completed_blocks(current_user))

    if latest_location.block_id == 'confirmation':

        this_location = Location(SchemaHelper.get_first_group_id(g.schema_json), 0, 'confirmation')

        block = SchemaHelper.get_block_for_location(g.schema_json, this_location)

        return _render_template({"block": block}, current_location=latest_location)

    metadata = get_metadata(current_user)

    return redirect(latest_location.url(metadata))


@questionnaire_blueprint.route('thank-you', methods=["GET"])
@login_required
def get_thank_you(eq_id, form_type, collection_id):
    thank_you_page = _render_template({}, block_id='thank-you')

    if not _check_same_survey(eq_id, form_type, collection_id):
        return redirect("/information/multiple-surveys")

    # Delete user data on request of thank you page.
    _delete_user_data()
    return thank_you_page


@questionnaire_blueprint.route('submit-answers', methods=["POST"])
@login_required
def submit_answers(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)

    answer_store = get_answer_store(current_user)
    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    submitter = SubmitterFactory.get_submitter()
    message = convert_answers(metadata, g.schema, answer_store, path_finder.get_routing_path())
    submitter.send_answers(message)

    logger.info("Responses submitted tx_id=%s", metadata["tx_id"])
    return redirect_to_thank_you(eq_id, form_type, collection_id)


@questionnaire_blueprint.route('<group_id>/<int:group_instance>/permanent-or-family-home', methods=["POST"])
@login_required
def post_everyone_at_address_confirmation(eq_id, form_type, collection_id, group_id, group_instance):
    if request.form.get('permanent-or-family-home-answer') == 'No':
        _remove_repeating_on_household_answers(get_answer_store(current_user), group_id)
    return post_block(eq_id, form_type, collection_id, group_id, group_instance, 'permanent-or-family-home')


def _remove_repeating_on_household_answers(answer_store, group_id):
    answer_store.remove(group_id=group_id, block_id='household-composition')
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    for answer in SchemaHelper.get_answers_that_repeat_in_block(g.schema_json, 'household-composition'):
        groups_to_delete = SchemaHelper.get_groups_that_repeat_with_answer_id(g.schema_json, answer['id'])
        for group in groups_to_delete:
            answer_store.remove(group_id=group['id'])
            questionnaire_store.completed_blocks[:] = [b for b in questionnaire_store.completed_blocks if
                                                       b.group_id != group['id']]


def update_questionnaire_store(location, answer_dict):
    # Store answers in QuestionnaireStore
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)

    survey_answer_ids = SchemaHelper.get_answer_ids_for_location(g.schema_json, location)

    for answer_id, answer_value in answer_dict.items():
        if answer_id in survey_answer_ids or location.block_id == 'household-composition':
            # Dates are comprised of 3 string values
            if isinstance(answer_value, dict) and 'day' in answer_value and 'month' in answer_value:
                datestr = "{:02d}/{:02d}/{}".format(int(answer_value['day']), int(answer_value['month']), answer_value['year'])
                answer = Answer(answer_id=answer_id, value=datestr, location=location)
            elif isinstance(answer_value, dict) and 'year' in answer_value and 'month' in answer_value:
                datestr = "{:02d}/{}".format(int(answer_value['month']), answer_value['year'])
                answer = Answer(answer_id=answer_id, value=datestr, location=location)
            else:
                answer = Answer(answer_id=answer_id, value=answer_value, location=location)
            questionnaire_store.answer_store.add_or_update(answer)

    if location not in questionnaire_store.completed_blocks:
        questionnaire_store.completed_blocks.append(location)


def _delete_user_data():
    get_questionnaire_store(current_user.user_id, current_user.user_ik).delete()
    session_storage.clear()


def redirect_to_thank_you(eq_id, form_type, collection_id):
    return redirect(interstitial_url(eq_id, form_type, collection_id, 'thank-you'))


def redirect_to_confirmation(eq_id, form_type, collection_id):
    return redirect(interstitial_url(eq_id, form_type, collection_id, 'confirmation'))


def interstitial_url(eq_id, form_type, collection_id, block_id):
    if block_id == 'summary':
        return url_for('.get_summary',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'introduction':
        return url_for('.get_introduction',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'confirmation':
        return url_for('.get_confirmation',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)
    elif block_id == 'thank-you':
        return url_for('.get_thank_you',
                       eq_id=eq_id,
                       form_type=form_type,
                       collection_id=collection_id)


def _check_same_survey(eq_id, form_type, collection_id):
    metadata = get_metadata(current_user)
    current_survey = eq_id + form_type + collection_id
    metadata_survey = metadata["eq_id"] + metadata["form_type"] + metadata["collection_exercise_sid"]
    if current_survey != metadata_survey:
        raise MultipleSurveyError


def _render_template(context, current_location=None, block_id=None, template=None):
    metadata = get_metadata(current_user)
    metadata_context = build_metadata_context(metadata)

    answer_store = get_answer_store(current_user)
    completed_blocks = get_completed_blocks(current_user)

    path_finder = PathFinder(g.schema_json, answer_store, metadata)
    navigation = Navigation(g.schema_json, answer_store, metadata, completed_blocks)

    if current_location is None:
        group_id = SchemaHelper.get_first_group_id(g.schema_json)
        current_location = Location(group_id, 0, block_id)

    previous_location = path_finder.get_previous_location(current_location)
    front_end_navigation = navigation.build_navigation(current_location.group_id, current_location.group_instance)

    previous_url = None

    if previous_location is not None and current_location.block_id != SchemaHelper.get_first_block_id_for_group(g.schema_json, current_location.group_id):
        previous_url = previous_location.url(metadata)

    try:
        theme = g.schema_json['theme']
        logger.debug("Theme selected: %s", theme)
    except KeyError:
        logger.info("No theme set")
        theme = None

    template = '{}.html'.format(template or current_location.block_id)

    return render_theme_template(theme, template,
                                 meta=metadata_context,
                                 content=context,
                                 current_location=current_location,
                                 previous_location=previous_url,
                                 navigation=front_end_navigation,
                                 schema_title=g.schema_json['title'])
