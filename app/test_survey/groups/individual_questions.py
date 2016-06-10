from app.model.group import Group

from app.test_survey.pages.page7 import page7
from app.test_survey.pages.page8 import page8

individual_questions = Group()
individual_questions.id = 'individual-questions'
individual_questions.title = ''

individual_questions.add_block(page7)
individual_questions.add_block(page8)
