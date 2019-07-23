build:
	pipenv run ./scripts/build.sh

lint:
	pipenv run ./scripts/run_lint.sh

test:
	pipenv run ./scripts/run_tests.sh

test-unit:
	pipenv run ./scripts/run_tests_unit.sh

test-functional:
	pipenv run ./scripts/run_tests_functional.sh

test-schemas:
	pipenv run ./scripts/test_schemas.sh

translate:
	pipenv run pybabel compile -d app/translations
	pipenv run python -m scripts.translate_schemas

translation-templates:
	pipenv run python -m scripts.extract_translation_templates

test-translation-templates:
	pipenv run python -m scripts.extract_translation_templates --test

load-templates:
	pipenv run ./scripts/load_templates.sh

run: build
	ln -sf .development.env .env
	pipenv run flask run

dev-compose-up:
	docker-compose pull eq-questionnaire-launcher
	docker-compose -f docker-compose-dev-mac.yml up -d

dev-compose-up-linux:
	docker-compose -f docker-compose-dev-linux.yml up -d

dev-compose-down:
	docker-compose -f docker-compose-dev-mac.yml down

dev-compose-down-linux:
	docker-compose -f docker-compose-dev-linux.yml down

profile:
	pipenv run python profile_application.py

travis:
	ln -sf .development.env .env
	pipenv run ./scripts/run_travis.sh
