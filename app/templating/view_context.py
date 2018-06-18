from flask import g
from flask_wtf import FlaskForm
from flask_babel import gettext as _

from app.globals import is_dynamodb_enabled
from app.helpers.form_helper import get_form_for_location
from app.templating.summary_context import build_summary_rendering_context
from app.templating.template_renderer import renderer
from app.templating.utils import get_title_from_titles


def build_view_context(block_type, metadata, answer_store, schema_context, rendered_block, current_location, form):
    variables = None
    if g.schema.json.get('variables'):
        variables = renderer.render(g.schema.json.get('variables'), **schema_context)

    if block_type in ('Summary', 'SectionSummary'):
        form = form or FlaskForm()

        return build_view_context_for_summary(metadata, answer_store, schema_context, block_type, variables,
                                              form.csrf_token, current_location)

    if block_type in ('Question', 'ConfirmationQuestion'):
        form = form or get_form_for_location(g.schema, rendered_block, current_location, answer_store, metadata)

        return build_view_context_for_question(metadata, answer_store, current_location, variables, rendered_block, form)

    if block_type in ('Introduction', 'Interstitial', 'Confirmation'):
        form = form or FlaskForm()
        return build_view_context_for_non_question(variables, form.csrf_token, rendered_block)


def build_view_context_for_non_question(variables, csrf_token, rendered_block):
    return {
        'variables': variables,
        'block': rendered_block,
        'csrf_token': csrf_token,
    }


def build_view_context_for_question(metadata, answer_store, current_location, variables, rendered_block, form):  # noqa: C901  pylint: disable=too-complex

    context = {
        'variables': variables,
        'block': rendered_block,
        'csrf_token': form.csrf_token,
        'question_titles': {},
        'form': {
            'errors': form.errors,
            'question_errors': form.question_errors,
            'mapped_errors': form.map_errors(),
            'answer_errors': {},
            'data': {},
            'other_answer': {},
            'fields': {}
        }

    }

    answer_ids = []
    for question in rendered_block.get('questions'):
        if question.get('titles'):
            context['question_titles'][question['id']] = get_title_from_titles(metadata, answer_store,
                                                                               question['titles'],
                                                                               current_location.group_instance)
        for answer in question['answers']:
            if current_location.block_id == 'household-composition':
                for repeated_form in form.household:
                    answer_ids.append(repeated_form.form[answer['id']].id)
            else:
                answer_ids.append(answer['id'])

            if answer['type'] in ('Checkbox', 'MutuallyExclusiveCheckbox', 'Radio'):
                options = answer['options']
                context['form']['other_answer'][answer['id']] = []
                for index in range(len(options)):
                    context['form']['other_answer'][answer['id']].append(form.get_other_answer(answer['id'], index))

    for answer_id in answer_ids:
        context['form']['answer_errors'][answer_id] = form.answer_errors(answer_id)

        if hasattr(form, 'get_data'):
            context['form']['data'][answer_id] = form.get_data(answer_id)

        if answer_id in form:
            context['form']['fields'][answer_id] = form[answer_id]

    if current_location.block_id in ['household-composition']:
        context['form']['household'] = form.household

    return context


def build_view_context_for_summary(metadata, answer_store, schema_context, block_type, variables, csrf_token,
                                   current_location):
    section_list = []
    title = None

    if block_type == 'Summary':
        section_list = renderer.render(g.schema.json, **schema_context)['sections']
        title = _('Your answers')

    elif block_type == 'SectionSummary':
        for section in g.schema.json['sections']:
            group_ids = (group['id'] for group in section['groups'])
            if current_location.group_id in group_ids:
                section_list = [renderer.render(section, **schema_context)]
                title = section['title']
                break

    summary_rendering_context = build_summary_rendering_context(g.schema, section_list, answer_store, metadata)

    context = {
        'csrf_token': csrf_token,
        'summary': {
            'groups': summary_rendering_context,
            'answers_are_editable': True,
            'is_view_submission_response_enabled': is_view_submitted_response_enabled(g.schema.json),
            'summary_type': block_type,
            'title': title,
        },
        'variables': variables,
    }
    return context


def is_view_submitted_response_enabled(schema):
    if not is_dynamodb_enabled():
        view_submitted_response = schema.get('view_submitted_response')
        if view_submitted_response:
            return view_submitted_response['enabled']

    return False
