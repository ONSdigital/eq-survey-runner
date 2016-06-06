from app.model.group import Group

from app.test_survey.pages.page3 import page3
# from app.test_survey.pages.page4 import page4
# from app.test_survey.pages.page5 import page5
from app.test_survey.pages.page6 import page6

household_questions = Group()
household_questions.id = 'household-questions'
household_questions.title = ''

household_questions.add_block(page3)

# household_questions.add_block(page4)
# household_questions.add_block(page5)
household_questions.add_block(page6)
