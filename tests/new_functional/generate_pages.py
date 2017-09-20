#!/usr/bin/env python

import argparse
import json
import logging
import os
import re
from string import Template

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description = 'Generate a bag of DOM selectors, organised by page, to make writing webdriver tests easier')
parser.add_argument('SCHEMA', type=argparse.FileType('r'),
                    help='The path to the schema file you want to generate pages for.')

parser.add_argument('OUT_DIRECTORY', help='The path to the directory where the pages should be written.')

parser.add_argument('-s', '--spec_file', help='The file where the template spec should be written.')

parser.add_argument('-r', '--require_path', default='..',
                    help='The relative path from a page file to the directory containing the base/parent page classes. Defaults to ".."')


SPEC_PAGE_HEADER = "const helpers = require('../helpers');\n\n"

SPEC_PAGE_IMPORT = Template(r"""const ${pageName}Page = require('../pages/${pageDir}/${pageFile}');
""")

SPEC_EXAMPLE_TEST = Template(r"""
describe('Example Test', function() {

  it('Given..., When..., Then...', function() {
    return helpers.openQuestionnaire('${schema}').then(() => {
        return browser    
    });
  });

});

""")

HEADER = Template(r"""// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const $basePage = require('$relativeRequirePath/$basePageFile');

""")

CLASS_NAME = Template(r"""class ${pageName}Page extends $basePage {

""")

ANSWER_LABEL_GETTER = Template(r"""  ${answerName}Label() { return '#label-${answerId}'; }

""")

ANSWER_GETTER = Template(r"""  ${answerName}() {
    return '#${answerId}';
  }

""")

HOUSEHOLD_ANSWER_GETTER = Template(r"""  ${answerName}(index = 0) {
    return '#household-' + index + '-${answerId}';
  }

""")

REPEATING_ANSWER_ADD_REMOVE = r"""  addPerson() {
    return 'button[name="action[add_answer]"]';
  }

  removePerson(index) {
    return 'button[value="' + index + '"]';
    // Have to check whether it's visible in test code
  }

"""

SUMMARY_ANSWER_GETTER = Template(r"""  ${answerName}() { return '#${answerId}-answer'; }

""")


SUMMARY_ANSWER_EDIT_GETTER = Template(r"""  ${answerName}Edit() { return '[data-qa="${answerId}-edit"]'; }

""")

CONSTRUCTOR = Template(r"""  constructor() {
    super('${block_id}');
  }

""")

FOOTER = Template(r"""}
module.exports = new ${pageName}Page();
""")


def generate_pascal_case_from_id(id_str):
    parts = re.sub('[^0-9a-zA-Z]+', '-', id_str).split('-')
    name = ''.join([p.title() for p in parts])
    return name

def camel_case(s):
    return s[0].lower() + s[1:]


def process_options(answer_id, options, page_spec, base_prefix):
    for index, option in enumerate(options):
        if option['value'][0].isalpha():
            prefix = base_prefix
        else:
            prefix = base_prefix + 'Answer'

        option_name = camel_case(prefix + generate_pascal_case_from_id(option['value']))
        option_id = "{name}-{index}".format(name=answer_id, index=index)

        option_context = {
            'answerName': option_name,
            'answerId': option_id
        }

        page_spec.write(ANSWER_GETTER.substitute(option_context))
        page_spec.write(ANSWER_LABEL_GETTER.substitute(option_context))

        # Add a selector for an option which exposes another input, e.g.
        # an 'Other' option which exposes a text input for the user to fill in
        if 'child_answer_id' in option:
            option_context = {
                'answerId': option['child_answer_id'],
                'answerName': prefix + option_name + 'Text'
            }

            page_spec.write(ANSWER_GETTER.substitute(option_context))


def process_answer(question_type, answer, page_spec, long_names, page_name):

    # If there's only one answer on the page shortcut the name space to improve
    # the quality of life of spec authors
    answer_name = generate_pascal_case_from_id(answer['id']) if long_names else 'answer'
    answer_name = answer_name.replace(page_name, '')
    answer_name = answer_name.replace('Answer', '')
    prefix = camel_case(answer_name) if len(answer_name) > 0 and long_names else ''

    if 'parent_answer_id' in answer:
        logger.debug("\t\tSkipping Child Answer: %s", answer['id'])
        return

    elif answer['type'] in ('Radio', 'Checkbox'):
        process_options(answer['id'], answer['options'], page_spec, prefix)

    elif answer['type'] in ('Date'):
        page_spec.write(_write_date_answer(answer_name, answer['id'], prefix))

    elif answer['type'] in ('MonthYearDate'):
        page_spec.write(_write_month_year_date_answer(answer_name, answer['id'], prefix))

    elif answer['type'] in ('TextField', 'Number', 'TextArea', 'Currency', 'Percentage', 'Relationship', 'Unit'):

        answer_context = {
            'answerName': camel_case(answer_name),
            'answerId': answer['id']
        }

        if question_type in ['RepeatingAnswer']:
            page_spec.write(HOUSEHOLD_ANSWER_GETTER.substitute(answer_context))
        else:
            page_spec.write(ANSWER_GETTER.substitute(answer_context))
            page_spec.write(ANSWER_LABEL_GETTER.substitute(answer_context))

    else:
        raise Exception('Answer type {} not configured'.format(answer['type']))


def process_question(question, page_spec, num_questions, page_name):
    logger.debug("\t\tprocessing question: %s", question['title'])

    question_type = question['type']
    if question_type == 'RepeatingAnswer':
        page_spec.write(REPEATING_ANSWER_ADD_REMOVE)

    long_names = long_names_required(question, num_questions)

    for answer in question['answers']:
        process_answer(question_type, answer, page_spec, long_names, page_name)

def process_summary(schema_data, page_spec):
    for group in schema_data['groups']:
        for block in group['blocks']:
            for question in block.get('questions', []):
                for answer in question['answers']:
                    answer_name = generate_pascal_case_from_id(answer['id'])
                    answer_context = {
                        'answerName': camel_case(answer_name),
                        'answerId': answer['id']
                    }
                    page_spec.write(SUMMARY_ANSWER_GETTER.substitute(answer_context))
                    page_spec.write(SUMMARY_ANSWER_EDIT_GETTER.substitute(answer_context))


def long_names_required(question, num_questions):
    if num_questions > 1:
        return True
    else:
        num_answers = len(question['answers'])
        if num_answers == 2 and 'other' in question['answers'][1]['id']:
            num_answers = 1

        if num_answers > 1:
            return True

    return False

def _write_date_answer(answer_name, answerId, prefix):

    return \
        ANSWER_GETTER.substitute({'answerName': prefix + 'day', 'answerId': answerId + '-day'}) + \
        ANSWER_GETTER.substitute({'answerName': prefix + 'month', 'answerId': answerId + '-month'}) + \
        ANSWER_GETTER.substitute({'answerName': prefix + 'year', 'answerId': answerId + '-year'})


def _write_month_year_date_answer(answer_name, answerId, prefix):
    return \
        ANSWER_GETTER.substitute({'answerName': prefix + 'Month', 'answerId': answerId + '-month'}) + \
        ANSWER_GETTER.substitute({'answerName': prefix + 'answerYear', 'answerId': answerId + '-year'})


def find_kv(block, key, values):
    for question in block.get('questions', []):
        for answer in question.get('answers', []):
            if key in answer and answer[key] in values:
                return True

    return False


def process_block(block, dir_out, schema_data, spec_file, relative_require = '..'):
    logger.debug("Processing Block: %s", block['id'])

    page_filename = block['id'] + '.page.js'
    page_path = os.path.join(dir_out, page_filename)

    logger.info("creating %s...", page_path)

    with open(page_path, 'w') as page_spec:
        page_name = generate_pascal_case_from_id(block['id'])

        base_page = 'QuestionPage'
        base_page_file = 'question.page'

        block_context = {
            'pageName': page_name,
            'basePage': base_page,
            'basePageFile': base_page_file,
            'pageDir': dir_out.split('pages/')[1],
            'pageFile': page_filename,
            'block_id': block['id'],
            'relativeRequirePath': relative_require
        }

        page_spec.write(HEADER.substitute(block_context))
        page_spec.write(CLASS_NAME.substitute(block_context))
        page_spec.write(CONSTRUCTOR.substitute(block_context))

        if block['type'] == 'Summary':
            process_summary(schema_data, page_spec)
        else:
            num_questions = len(block.get('questions', []))

            for question in block.get('questions', []):
                process_question(question, page_spec, num_questions, page_name)


        page_spec.write(FOOTER.substitute(block_context))

        if spec_file:
            with open(spec_file, 'a') as template_spec:
                template_spec.write(SPEC_PAGE_IMPORT.substitute(block_context))


def process_schema(in_schema, out_dir, spec_file, require_path='..'):

    data = json.loads(in_schema.read())

    try:
        os.stat(out_dir)
    except:
        os.mkdir(out_dir)

    for group in data['groups']:
        for block in group['blocks']:
            process_block(block, out_dir, data, spec_file, require_path)


if __name__ == '__main__':
    args = parser.parse_args()

    spec_file = args.spec_file

    if spec_file:
        with open(spec_file, 'w') as template_spec:
            template_spec.write(SPEC_PAGE_HEADER)
            template_spec.close()

            process_schema(args.SCHEMA, args.OUT_DIRECTORY, spec_file, args.require_path)

            with open(spec_file, 'a') as template_spec:
                schema_name = { 'schema': args.SCHEMA.name.split('/').pop() }
                template_spec.write(SPEC_EXAMPLE_TEST.substitute(schema_name))
    else:
        process_schema(args.SCHEMA, args.OUT_DIRECTORY, spec_file, args.require_path)
