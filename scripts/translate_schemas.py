import logging
import os
import sys

import docker

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

TRANSLATION_MAP = {'cy': ['census_individual_gb_wls']}


def translate_schemas():
    docker_client = docker.from_env()

    for language, schemas in TRANSLATION_MAP.items():
        for schema_name in schemas:
            translation_file = f'{schema_name}_{language}.po'
            schema_file = f'{schema_name}.json'
            relative_dir = f'data/{language}'
            output_dir = f'/usr/src/eq-survey-runner/data/{language}'
            language_dir = f'/usr/src/eq-survey-runner/app/translations/{language}'

            logger.info('Building %s/%s', relative_dir, schema_file)

            os.makedirs(relative_dir, exist_ok=True)

            docker_client.images.pull('onsdigital/eq-translations:latest')
            container = docker_client.containers.run(
                'onsdigital/eq-translations',
                f'pipenv run python -m cli.translate_survey ../eq-survey-runner/data/en/{schema_file} {language_dir}/{translation_file} {output_dir}',
                volumes={
                    os.getcwd(): {'bind': '/usr/src/eq-survey-runner', 'mode': 'rw'}
                },
                remove=True,
                detach=True,
            )
            for log in container.logs(stdout=True, stream=True):
                logger.info(log.decode().strip('\n'))


if __name__ == '__main__':
    translate_schemas()
