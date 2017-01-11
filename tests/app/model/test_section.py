import unittest

from app.schema.question import Question
from app.schema.section import Section


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

        self.assertEqual(section.id, 'some-id')
        self.assertEqual(section.title, 'my section object')
        self.assertIsNone(section.container)
        self.assertEqual(len(section.questions), 2)
        self.assertEqual(section.questions[0], question1)
        self.assertEqual(section.questions[1], question2)

        self.assertEqual(question1.container, section)
        self.assertEqual(question2.container, section)
