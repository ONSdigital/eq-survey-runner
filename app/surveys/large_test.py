from app.schema.questionnaire import Questionnaire

# Create the Questionnaire
test_questionnaire = Questionnaire()
large_test = test_questionnaire
large_test.eq_id = '0'
form_type = '2011'

# Do the imports here to prevent circular dependencies
from app.surveys.large_components.groups.household_questions import household_questions  # NOQA
from app.surveys.large_components.groups.individual_questions import individual_questions  # NOQA

# Set the questionnaire properties
test_questionnaire.id = "questionnaire"
test_questionnaire.survey_id = "Test_Survey"
test_questionnaire.title = "Test Survey"
test_questionnaire.description = "eQ Test survey"

# Add the groups
test_questionnaire.add_group(household_questions)
test_questionnaire.register(household_questions)

test_questionnaire.add_group(individual_questions)
test_questionnaire.register(individual_questions)
