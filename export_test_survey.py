import json
from app.test_survey.test_survey import test_questionnaire

with open('app/data/99_test_survey.json', 'w') as file:
    file.write(json.dumps(test_questionnaire.to_json()))

print("Done")  # NOQA
