#!/usr/bin/env python

import argparse
import json
from copy import deepcopy
from glob import iglob
from yaml import safe_load


def generate_schema(manifest, survey):
    schema = {'groups': []}

    for group in manifest['groups']:
        new_group = deepcopy(group)
        new_group['blocks'] = []
        schema['groups'].append(new_group)

        for block_id in group['blocks']:
            block = deepcopy(survey['blocks'][block_id])
            new_group['blocks'].append(block)

            if 'questions' not in survey['blocks'][block_id]:
                continue

            del block['questions']
            block['questions'] = []

            for question in survey['blocks'][block_id]['questions']:
                block['questions'].append(question)

    for key, value in manifest.items():
        if key not in ['groups', 'schema_filename']:
            schema[key] = value

    return schema


def merge_block_files(files):
    survey = {'blocks': {}}
    for filepath in files:
        with open(filepath) as block:
            block = safe_load(block)

        name_start_index = filepath.rindex('/') + 1
        name_end_index = filepath.rindex('.')
        block_key = filepath[name_start_index:name_end_index]
        survey['blocks'][block_key] = block

    return survey


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Mills out all the schema variants defined in the manifest files'
    )

    parser.add_argument(
        'SOURCES_DIR', help='The directory that contains the manifests and blocks'
    )

    parser.add_argument(
        'OUT_DIR', help='The location where generated schemas should be written'
    )

    args = parser.parse_args()
    out_dir = args.OUT_DIR.rstrip('/')
    sources_dir = args.SOURCES_DIR.rstrip('/')

    surveys = iglob(sources_dir + '/manifests/**/')

    for survey_path in surveys:

        survey_name = survey_path.split('/')[-2]

        blocks = iglob('{}/blocks/{}/*.yaml'.format(sources_dir, survey_name))
        merged_blocks = merge_block_files(blocks)

        manifest_paths = iglob(survey_path + '/*.yaml')

        for path in manifest_paths:
            with open(path) as manifest_file:
                manifest = safe_load(manifest_file)

            if 'schema_filename' not in manifest:
                print(  # noqa: T001,T101
                    "WARNING - No 'schema_filename' found in {}, skipping to the next one.".format(
                        path
                    )
                )
                continue

            schema = generate_schema(manifest, merged_blocks)

            file_name = '{}/{}.json'.format(
                out_dir, manifest['schema_filename'], 'json'
            )

            out = open(file_name, 'w')

            json.dump(schema, out, indent=2)

            print("Built {}".format(file_name))  # noqa: T003
