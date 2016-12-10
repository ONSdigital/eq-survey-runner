import datetime
import json
import logging
import os
import sys
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


SPEC_PAGE_HEADER = r"""import chai from 'chai'
import {startQuestionnaire} from '../helpers'

"""

SPEC_PAGE_IMPORT = r"""import {pageName} from '../pages/{pageDir}{pageFile}'
"""

SPEC_CHAI_HEADER = r"""
const expect = chai.expect
"""

SPEC_EXAMPLE_TEST = r"""
describe('Example Test', function() {

  it('Given..., When..., Then...', function() {
    startQuestionnaire('{schema}')
  })

})

"""

HEADER = r"""// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON {generated} - DO NOT EDIT!!! <<<

import {basePage} from '../../{basePageFile}'

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

FOOTER = r"""}

export default new {pageName}Page()
"""


def generate_camel_case_from_id(id_str):
    parts = re.sub('[^0-9a-zA-Z]+', '-', id_str).split('-')
    name = ''.join([p.title() for p in parts])
    return name


def process_options(answer_id, options, page_spec):
    for index, option in enumerate(options):
        option_name = generate_camel_case_from_id(option['value'])
        option_id = "{name}-{index}".format(name=answer_id, index=index+1)
        page_spec.write(CHECKBOX_RADIO_CLICKER.replace("{optionName}", generate_camel_case_from_id(answer_id) + option_name).replace("{optionId}", option_id))


def process_answer(answer, page_spec):
    if answer['type'] == 'Radio' or answer['type'] == 'Checkbox':
        process_options(answer['id'], answer['options'], page_spec)

    elif answer['type'] == 'Date':
        answer_name = generate_camel_case_from_id(answer['id'])
        page_spec.write(_write_date_answer(answer_name, answer['id']))

    elif answer['type'] == 'MonthYearDate':
        answer_name = generate_camel_case_from_id(answer['id'])
        page_spec.write(_write_month_year_date_answer(answer_name, answer['id']))

    elif (answer['type'] == 'TextField' or answer['type'] == 'Integer' or
            answer['type'] == 'PositiveInteger' or answer['type'] == 'TextArea'):
        answer_name = generate_camel_case_from_id(answer['id'])
        page_spec.write(ANSWER_SETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))
        page_spec.write(ANSWER_GETTER.replace("{answerName}", answer_name).replace("{answerId}", answer['id']))

    else:
        raise Exception('Answer type [%s] not configured' % answer['type'])


def process_question(question, page_spec):
    logger.debug("\t\tProcessing Question: %s", question['title'])

    for answer in question['answers']:
        process_answer(answer, page_spec)


def process_section(section, page_spec):
    logger.debug("\tProcessing Section: %s", section['title'])

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
    for section in block['sections']:
        for question in section['questions']:
            for answer in question['answers']:
                if key in answer and answer[key] in values:
                    return True

    return False


def process_block(block, dir_out, spec_out):
    logger.debug("Processing Block: %s", block['id'])

    page_filename = block['id'] + '.page.js'
    page_path = os.path.join(dir_out, page_filename)

    logger.info("Creating %s...", page_path)

    with open(page_path, 'w') as page_spec:
        multiple_choice_check = find_kv(block, 'type', ['Radio', 'Checkbox'])

        page_name = generate_camel_case_from_id(block['id'])

        header = HEADER
        header = header.replace("{generated}", str(datetime.datetime.now()))
        header = header.replace("{basePage}", "QuestionPage" if not multiple_choice_check else "MultipleChoiceWithOtherPage")
        header = header.replace("{basePageFile}", "question.page" if not multiple_choice_check else "multiple-choice.page")

        page_spec.write(header)

        class_name = CLASS_NAME
        class_name = class_name.replace("{pageName}", page_name)
        class_name = class_name.replace("{basePage}", "QuestionPage" if not multiple_choice_check else "MultipleChoiceWithOtherPage")
        class_name = class_name.replace("{basePageFile}", "question.page" if not multiple_choice_check else "multiple-choice.page")

        page_spec.write(class_name)

        for section in block['sections']:
            process_section(section, page_spec)

        page_spec.write(FOOTER.replace("{pageName}", page_name))

        with open(spec_out, 'a') as template_spec:
            header = SPEC_PAGE_IMPORT
            header = header.replace("{pageDir}", dir_out.split('pages/')[1])
            header = header.replace("{pageName}", page_name)
            header = header.replace("{pageFile}", page_filename)
            template_spec.write(header)



def process_schema(in_schema, out_dir, spec_out):

    json_data = open(in_schema).read()
    data = json.loads(json_data)

    for group in data['groups']:
        for block in group['blocks']:
            process_block(block, out_dir, spec_out)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: {} <schema.json> </outdir/> <spec_out>".format(sys.argv[0]))
        print("Example: {} ./app/data/census_household.json ./tests/functional/pages/surveys/census/ ./tests/functional/spec/census-test.spec.js".format(sys.argv[0]))
        exit(1)

    schema_in = sys.argv[1]
    dir_out = sys.argv[2]
    spec_out = sys.argv[3]

    with open(spec_out, 'w') as template_spec:
        template_spec.write(SPEC_PAGE_HEADER)

    process_schema(schema_in, dir_out, spec_out)

    with open(spec_out, 'a') as template_spec:
        template_spec.write(SPEC_CHAI_HEADER)
        template_spec.write(SPEC_EXAMPLE_TEST.replace("{schema}", schema_in.split('/').pop()))
