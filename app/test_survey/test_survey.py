from app.model.questionnaire import Questionnaire

# Create the Questionnaire
test_questionnaire = Questionnaire()

# Do the imports here to prevent circular dependencies
from app.test_survey.groups.household_questions import household_questions  # NOQA

# Set the questionnaire properties
test_questionnaire.id = "questionnaire"
test_questionnaire.survey_id = "Test_Survey"
test_questionnaire.title = "Test Survey"
test_questionnaire.description = "eQ Test survey"

# Add the groups
test_questionnaire.add_group(household_questions)
test_questionnaire.register(household_questions)
