import json

from app.questionnaire.questionnaire_schema import QuestionnaireSchema


def check_answer_values():
    for schema_filename in [
        'census_individual_gb_eng.json',
        'census_household_gb_eng.json',
        'census_individual_gb_nir.json',
        'census_household_gb_nir.json',
    ]:
        with open(f'data/en/{schema_filename}') as schema_file:
            found_options = {}
            data = json.load(schema_file)
            schema = QuestionnaireSchema(data)
            for answers in schema.get_answer_ids():
                for answer in answers:
                    if 'options' in answer:
                        for option in answer['options']:
                            if option['value'] != option['label']:
                                found_options[answer['id']] = option

            print(f"-----------------")
            print(
                "{schema_filename}: {number} differences\n".format(
                    number=len(found_options), schema_filename=schema_filename
                )
            )

            for answer_id, option in found_options.items():
                print(f"{answer_id} : '{option['label']}' : '{option['value']}'")


if __name__ == '__main__':
    check_answer_values()
