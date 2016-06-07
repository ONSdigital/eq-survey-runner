from app.model.section import Section
from app.model.question import Question
import unittest
import json


class SectionModelTest(unittest.TestCase):
    def test_basics(self):
        section = Section()

        section.id = 'some-id'
        section.title = 'my section object'

        question1 = Question()
        question1.id = 'question-1'
        question2 = Question()
        question2.id = 'question-2'

        section.add_question(question1)
        section.add_question(question2)

        self.assertEquals(section.id, 'some-id')
        self.assertEquals(section.title, 'my section object')
        self.assertIsNone(section.container)
        self.assertEquals(len(section.questions), 2)
        self.assertEquals(section.questions[0], question1)
        self.assertEquals(section.questions[1], question2)

        self.assertEquals(question1.container, section)
        self.assertEquals(question2.container, section)

    def test_to_json(self):
        section = Section()

        section.id = 'some-id'
        section.title = 'my section object'

        question1 = Question()
        question1.id = 'question-1'
        question2 = Question()
        question2.id = 'question-2'

        section.add_question(question1)
        section.add_question(question2)

        json_str = json.dumps(section.to_json())
        json_obj = json.loads(json_str)

        self.assertEquals(json_obj['id'], 'some-id')
        self.assertEquals(json_obj['title'], 'my section object')
        self.assertEquals(len(json_obj['questions']), 2)

    def test_equivalence(self):
        section1 = Section()

        section1.id = 'some-id'
        section1.title = 'my section object'

        question1_1 = Question()
        question1_1.id = 'question-1'
        question1_2 = Question()
        question1_2.id = 'question-2'

        section1.add_question(question1_1)
        section1.add_question(question1_2)

        section2 = Section()

        section2.id = 'some-id'
        section2.title = 'my section object'

        question2_1 = Question()
        question2_1.id = 'question-1'
        question2_2 = Question()
        question2_2.id = 'question-2'

        section2.add_question(question2_1)
        section2.add_question(question2_2)

        self.assertEquals(section1, section2)
