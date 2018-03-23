from flask import g
from flask_wtf import FlaskForm

from app.globals import is_dynamodb_enabled
from app.helpers.form_helper import get_form_for_location
from app.templating.summary_context import build_summary_rendering_context
from app.templating.template_renderer import renderer


def build_view_context(metadata, answer_store, schema_context, block, current_location, form):

    variables = None
    if g.schema.json.get('variables'):
        variables = renderer.render(g.schema.json.get('variables'), **schema_context)

    rendered_block = renderer.render(block, **schema_context)

    if block['type'] in ('Summary', 'SectionSummary'):
        form = form or FlaskForm()

        return build_view_context_for_summary(metadata, answer_store, schema_context, variables, form.csrf_token)

    if block['type'] in ('Question', 'ConfirmationQuestion'):
        if not form:
            form = get_form_for_location(g.schema, rendered_block, current_location, answer_store)

        return build_view_context_for_question(current_location, variables, rendered_block, form)

    if block['type'] in ('Introduction', 'Interstitial', 'Confirmation'):
        form = form or FlaskForm()
        return build_view_context_for_non_question(variables, form.csrf_token, rendered_block)


def build_view_context_for_non_question(variables, csrf_token, rendered_block):
    return {
        'variables': variables,
        'block': rendered_block,
        'csrf_token': csrf_token,
    }


def build_view_context_for_question(current_location, variables, rendered_block, form):  # noqa: C901  pylint: disable=too-complex

    context = {
        'variables': variables,
        'block': rendered_block,
        'csrf_token': form.csrf_token,
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
        for answer in question['answers']:
            if current_location.block_id == 'household-composition':
                for repeated_form in form.household:
                    answer_ids.append(repeated_form.form[answer['id']].id)
            else:
                answer_ids.append(answer['id'])

            if answer['type'] in ('Checkbox', 'Radio'):
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


def build_view_context_for_summary(metadata, answer_store, schema_context, variables, csrf_token):
    rendered_schema_json = renderer.render(g.schema.json, **schema_context)
    summary_rendered_context = build_summary_rendering_context(g.schema, rendered_schema_json['sections'],
                                                               answer_store, metadata)

    context = {
        'csrf_token': csrf_token,
        'summary': {
            'groups': summary_rendered_context,
            'answers_are_editable': True,
            'is_view_submission_response_enabled': is_view_submitted_response_enabled(g.schema.json),
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
