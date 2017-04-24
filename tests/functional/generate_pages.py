import datetime
import json
import logging
import os
import sys
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


SPEC_PAGE_HEADER = r"""import {startQuestionnaire} from '../helpers'

"""

SPEC_PAGE_IMPORT = r"""import {pageName} from '../pages/{pageDir}{pageFile}'
"""

SPEC_EXAMPLE_TEST = r"""
describe('Example Test', function() {

  it('Given..., When..., Then...', function() {
    startQuestionnaire('{schema}')
  })

})

"""

HEADER = r"""// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import {basePage} from '../{basePageFile}'

"""

CLASS_NAME = r"""class {pageName}Page extends {basePage} {

"""

ANSWER_SETTER = r"""  set{answerName}(value) {
    browser.setValue('[name="{answerId}"]', value)
    return this
  }

"""

ANSWER_GETTER = r"""  get{answerName}(value) {
    return browser.element('[name="{answerId}"]').getValue()
  }

"""

ANSWER_LABEL_GETTER = r"""  get{answerName}Label() {
    return browser.element('#label-{answerId}')
  }

"""

ANSWER_ELEMENT_GETTER = r"""  get{answerName}Element() {
    return browser.element('[name="{answerId}"]')
  }

"""

DROP_DOWN_SETTER = r"""  set{answerName}(value) {
    browser.selectByValue('[name="{answerId}"]', value)
    return this
  }

"""

CHECKBOX_RADIO_CLICKER = r"""  click{optionName}() {
    browser.element('[id="{optionId}"]').click()
    return this
  }

"""

CHECKBOX_RADIO_IS_SELECTED = r"""  {optionName}IsSelected() {
    return browser.element('[id="{optionId}"]').isSelected()
  }

"""

MULTIPLE_CHOICE_OTHER = r"""  set{answerName}(value) {
    browser.setValue('[id="{answerId}"]', value)
    return this
  }

"""

RELATIONSHIP_DROPDOWN_SETTER = r"""  set{optionName}(instance = 0) {
    browser.selectByValue('[name="{answerId}-' + instance + '"]', '{optionValue}')
    return this
  }

"""

REPEATING_ANSWER_SETTER = r"""  set{answerName}(value, index = 0) {
    var field = 'household-' + index + '-{answerId}'
    browser.setValue('[name="' + field + '"]', value)
    return this
  }

"""

REPEATING_ANSWER_GETTER = r"""  get{answerName}(index) {
    var field = 'household-' + index + '-{answerId}'
    browser.element('[name="' + field + '"]').getValue()
    return this
  }

"""

REPEATING_ANSWER_ADD_REMOVE = r"""  addPerson() {
    browser.click('button[name="action[add_answer]"]')
    return this
  }

  removePerson(index) {
    browser.click('button[value="' + index + '"]')
    browser.waitUntil(() => {
      return !browser.isVisible('button[value="' + index + '"]')
    }, 5000, 'Person not removed')
    return this
  }

"""

CONSTRUCTOR = r"""  constructor() {
    super('{block_id}')
  }

"""

FOOTER = r"""}

export default new {pageName}Page()
"""


def generate_camel_case_from_id(id_str):
    parts = re.sub('[^0-9a-zA-Z]+', '-', id_str).split('-')
    name = ''.join([p.title() for p in parts])
    return name


def process_options(answer_id, options, template_setter, template_getter, page_spec):
    for index, option in enumerate(options):
        option_name = generate_camel_case_from_id(answer_id) + generate_camel_case_from_id(option['value'])
        option_id = "{name}-{index}".format(name=answer_id, index=index)
        page_spec.write(template_setter.replace("{optionName}", option_name).replace("{optionId}", option_id))
        page_spec.write(template_getter.replace("{optionName}", option_name).replace("{optionId}", option_id))
        if 'child_answer_id' in option:
            option_other_id = option['child_answer_id']
            page_spec.write(MULTIPLE_CHOICE_OTHER.replace("{answerName}", option_name + "Text").replace("{answerId}", option_other_id))


def process_relationship_options(answer_id, options, template, page_spec):
    for index, option in enumerate(options):
        option_name = generate_camel_case_from_id(option['value'])
        option_index = "{index}".format(index=index)
        template_with_index = template.replace("{optionIndex}", option_index)
        template_with_answer_id = template_with_index.replace("{answerId}", answer_id)
        template_with_option_value = template_with_answer_id.replace("{optionValue}", option['value'])
        template_with_option_name = template_with_option_value.replace("{optionName}", generate_camel_case_from_id(answer_id) + option_name)
        page_spec.write(template_with_option_name)


def process_answer(question_type, answer, page_spec):
    answer_name = generate_camel_case_from_id(answer['id'])

    if 'parent_answer_id' in answer:
        logger.debug("\t\tSkipping Child Answer: %s", answer['id'])
        return
    elif answer['type'] == 'Radio' or answer['type'] == 'Checkbox':
        process_options(answer['id'], answer['options'], CHECKBOX_RADIO_CLICKER, CHECKBOX_RADIO_IS_SELECTED, page_spec)
    elif answer['type'] == 'Relationship':
        process_relationship_options(answer['id'], answer['options'], RELATIONSHIP_DROPDOWN_SETTER, page_spec)
    elif answer['type'] == 'Date':
        page_spec.write(_write_date_answer(answer_name, answer['id']))

    elif answer['type'] == 'MonthYearDate':
        page_spec.write(_write_month_year_date_answer(answer_name, answer['id']))

    elif answer['type'] in ['TextField', 'Integer', 'PositiveInteger', 'TextArea', 'Currency', 'Percentage']:
        if question_type == 'RepeatingAnswer':
            page_spec.write(REPEATING_ANSWER_SETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))
            page_spec.write(REPEATING_ANSWER_GETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))
        else:
            page_spec.write(ANSWER_SETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))
            page_spec.write(ANSWER_GETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))
            page_spec.write(ANSWER_LABEL_GETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))
            page_spec.write(ANSWER_ELEMENT_GETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))

    else:
        raise Exception('Answer type [%s] not configured' % answer['type'])


def process_question(question, page_spec):
    logger.debug("\t\tprocessing question: %s", question['title'])

    question_type = question['type']
    if question_type == 'RepeatingAnswer':
        page_spec.write(REPEATING_ANSWER_ADD_REMOVE)
    for answer in question['answers']:
        process_answer(question_type, answer, page_spec)


def process_section(section, page_spec):
    logger.debug("\tprocessing section: %s", section['title'])

    for question in section['questions']:
        process_question(question, page_spec)


def _write_date_answer(answer_name, answerId):
    return \
        ANSWER_SETTER.replace("{answerName}", answer_name + 'Day').replace("{answerId}", answerId + '-day') + \
        ANSWER_GETTER.replace("{answerName}", answer_name + 'Day').replace("{answerId}", answerId + '-day') + \
        DROP_DOWN_SETTER.replace("{answerName}", answer_name + 'Month').replace("{answerId}", answerId + '-month') + \
        ANSWER_GETTER.replace("{answerName}", answer_name + 'Month').replace("{answerId}", answerId + '-month') + \
        ANSWER_SETTER.replace("{answerName}", answer_name + 'Year').replace("{answerId}", answerId + '-year') + \
        ANSWER_GETTER.replace("{answerName}", answer_name + 'Year').replace("{answerId}", answerId + '-year')


def _write_month_year_date_answer(answer_name, answerId):
    return \
        DROP_DOWN_SETTER.replace("{answerName}", answer_name + 'Month').replace("{answerId}", answerId + '-month') + \
        ANSWER_GETTER.replace("{answerName}", answer_name + 'Month').replace("{answerId}", answerId + '-month') + \
        ANSWER_SETTER.replace("{answerName}", answer_name + 'Year').replace("{answerId}", answerId + '-year') + \
        ANSWER_GETTER.replace("{answerName}", answer_name + 'Year').replace("{answerId}", answerId + '-year')


def find_kv(block, key, values):
    for section in block.get('sections', []):
        for question in section.get('questions', []):
            for answer in question.get('answers', []):
                if key in answer and answer[key] in values:
                    return True

    return False


def process_block(block, dir_out, spec_out=None):
    logger.debug("Processing Block: %s", block['id'])

    page_filename = block['id'] + '.page.js'
    page_path = os.path.join(dir_out, page_filename)

    logger.info("creating %s...", page_path)

    with open(page_path, 'w') as page_spec:
        multiple_choice_check = find_kv(block, 'type', ['Radio', 'Checkbox', 'Relationship'])

        page_name = generate_camel_case_from_id(block['id'])

        header = HEADER
        header = header.replace("{basePage}", "QuestionPage" if not multiple_choice_check else "MultipleChoiceWithOtherPage")
        header = header.replace("{basePageFile}", "question.page" if not multiple_choice_check else "multiple-choice.page")

        page_spec.write(header)

        class_name = CLASS_NAME
        class_name = class_name.replace("{pageName}", page_name)
        class_name = class_name.replace("{basePage}", "QuestionPage" if not multiple_choice_check else "MultipleChoiceWithOtherPage")
        class_name = class_name.replace("{basePageFile}", "question.page" if not multiple_choice_check else "multiple-choice.page")

        page_spec.write(class_name)

        page_spec.write(CONSTRUCTOR.replace("{block_id}", block['id']))

        for section in block.get('sections', []):
            process_section(section, page_spec)

        page_spec.write(FOOTER.replace("{pageName}", page_name))

        if spec_out:
            with open(spec_out, 'a') as template_spec:
                header = SPEC_PAGE_IMPORT
                header = header.replace("{pageDir}", dir_out.split('pages/')[1])
                header = header.replace("{pageName}", page_name)
                header = header.replace("{pageFile}", page_filename)
                template_spec.write(header)


def process_schema(in_schema, out_dir, spec_out=None):

    json_data = open(in_schema).read()
    data = json.loads(json_data)

    for group in data['groups']:
        for block in group['blocks']:
            process_block(block, out_dir, spec_out)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <schema.json> </outdir/> <spec_out>".format(sys.argv[0]))
        print("Example: {} ./data/census_household.json ./tests/functional/pages/surveys/census/household/ ./tests/functional/spec/census-test.spec.js".format(sys.argv[0]))
        exit(1)

    schema_in = sys.argv[1]
    dir_out = sys.argv[2]

    if len(sys.argv) == 4:
        spec_out = sys.argv[3]

        with open(spec_out, 'w') as template_spec:
            template_spec.write(SPEC_PAGE_HEADER)

        process_schema(schema_in, dir_out, spec_out)

        with open(spec_out, 'a') as template_spec:
            template_spec.write(SPEC_EXAMPLE_TEST.replace("{schema}", schema_in.split('/').pop()))
    else:
        process_schema(schema_in, dir_out)
