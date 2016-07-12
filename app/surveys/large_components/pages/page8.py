from app.schema.block import Block
from app.schema.section import Section
from app.schema.question import Question
from app.schema.answer import Answer

from app.surveys.large_test import test_questionnaire

page8 = Block()
page8.id = 'page-8'
page8.title = "Individual questions - Continued"
test_questionnaire.register(page8)

# I15
i15_s = Section()
i15_s.id = "section-i15"

i15_q = Question()
i15_q.id = "question-i15"
i15_q.title = '(I15) How would you describe your national identity?'
i15_q.description = 'Select all that apply'
# TODO: Decide on Question Types and Answer Types
i15_q.type = "General"

i15_r1 = Answer()
i15_r1.id = "answer1-i15"
i15_r1.type = "Checkbox"
i15_r1.code = "I15"
i15_r1.options = [
    # @TODO: Should route to question 13
    {
        "value": "i15_a",
        "label": "English"
    },
    # @TODO: Should route to question 13
    {
        "value": "i15_b",
        "label": "Welsh"
    },
    # @TODO: Should route to question 13
    {
        "value": "i15_c",
        "label": "Scottish"
    },
    # @TODO: Should route to question 13
    {
        "value": "i15_d",
        "label": "Northern Irish"
    },
    {
        "value": "i15_e",
        "label": "British"
    },
    {
        "value": "i15_f",
        "label": "Other, write in"
    }
]

i15_r2 = Answer()
i15_r2.id = 'answer2-i15'
i15_r2.type = 'textfield'
i15_r2.code = "H14"

i15_q.add_answer(i15_r1)
i15_q.add_answer(i15_r2)
i15_s.add_question(i15_q)
page8.add_section(i15_s)
test_questionnaire.register(i15_s)
test_questionnaire.register(i15_q)
test_questionnaire.register(i15_r1)
test_questionnaire.register(i15_r2)

# I16
i16_s = Section()
i16_s.id = 'section-i16'

i16_q = Question()
i16_q.id = 'question-i16'
i16_q.title = "(I16) What is your ethnic group?"
i16_q.type = "General"

i16_r1 = Answer()
i16_r1.id = 'answer1-i16'
i16_r1.type = "Radio"
i16_r1.code = 'I16'
i16_r1.label = "White"
i16_r1.options = [
    {
        "value": "i16_a",
        "label": "English/Welsh/Scottish/Nortern Irish/Brtitish"
    },
    {
        "value": "i16_b",
        "label": "Irish"
    },
    {
        "value": "i16_c",
        "label": "Gypsy or Irish Traveller"
    },
    {
        "value": "i16_d",
        "label": "Irish"
    },
    {
        "value": "i16_e",
        "label": "Any other White background, write in"
    }
]

i16_r2 = Answer()
i16_r2.id = 'answer2-i16'
i16_r2.type = 'textfield'
i16_r2.code = "I16"

i16_q.add_answer(i16_r1)
i16_q.add_answer(i16_r2)

i16_r3 = Answer()
i16_r3.id = 'answer3-i16'
i16_r3.type = "Radio"
i16_r3.code = 'I16'
i16_r3.label = "Mixed/multiple ehthnic groups"
i16_r3.options = [
    {
        "value": "i16_f",
        "label": "White and Black Caribbean"
    },
    {
        "value": "i16_g",
        "label": "White and Black African"
    },
    {
        "value": "i16_h",
        "label": "White and Asian"
    },
    {
        "value": "i16_i",
        "label": "Any other Mixed/Multiple ethnic background, write in"
    }
]

i16_r4 = Answer()
i16_r4.id = 'answer4-i16'
i16_r4.type = 'textfield'
i16_r4.code = "I16"

i16_q.add_answer(i16_r3)
i16_q.add_answer(i16_r4)

i16_r5 = Answer()
i16_r5.id = 'answer5-i16'
i16_r5.type = "Radio"
i16_r5.code = 'I16'
i16_r5.label = "Asian/Asian British"
i16_r5.options = [
    {
        "value": "i16_j",
        "label": "Indian"
    },
    {
        "value": "i16_k",
        "label": "Pakistani"
    },
    {
        "value": "i16_l",
        "label": "Bangladeshi"
    },
    {
        "value": "i16_m",
        "label": "Chinese"
    },
    {
        "value": "i16_n",
        "label": "Any other Asian Background, write in"
    }
]

i16_r6 = Answer()
i16_r6.id = 'answer6-i16'
i16_r6.type = 'textfield'
i16_r6.code = "I16"

i16_q.add_answer(i16_r5)
i16_q.add_answer(i16_r6)

i16_r7 = Answer()
i16_r7.id = 'answer7-i16'
i16_r7.type = "Radio"
i16_r7.code = 'I16'
i16_r7.label = "Black/African/Caribbean/Black British"
i16_r7.options = [
    {
        "value": "i16_o",
        "label": "African"
    },
    {
        "value": "i16_p",
        "label": "Caribbean"
    },
    {
        "value": "i16_q",
        "label": "Any other Black/African/Caribbean background, write in"
    }
]

i16_r8 = Answer()
i16_r8.id = 'answer8-i16'
i16_r8.type = 'textfield'
i16_r8.code = "I16"

i16_r9 = Answer()
i16_r9.id = 'answer9-i16'
i16_r9.type = "Radio"
i16_r9.code = 'I16'
i16_r9.label = "Other ethnic group"
i16_r9.options = [
    {
        "value": "i16_r",
        "label": "Arab"
    },
    {
        "value": "i16_s",
        "label": "Any other ethnic group, write in"
    }
]

i16_r10 = Answer()
i16_r10.id = 'answer10-i16'
i16_r10.type = 'textfield'
i16_r10.code = "I16"

i16_q.add_answer(i16_r9)
i16_q.add_answer(i16_r10)

i16_s.add_question(i16_q)
page8.add_section(i16_s)
test_questionnaire.register(i16_s)
test_questionnaire.register(i16_q)
test_questionnaire.register(i16_r1)
test_questionnaire.register(i16_r2)
test_questionnaire.register(i16_r3)
test_questionnaire.register(i16_r4)
test_questionnaire.register(i16_r5)
test_questionnaire.register(i16_r6)
test_questionnaire.register(i16_r7)
test_questionnaire.register(i16_r8)
test_questionnaire.register(i16_r9)
test_questionnaire.register(i16_r10)

# I17 Intentionally left blank


# I18
i18_s = Section()
i18_s.id = "section-i18"

i18_q = Question()
i18_q.id = "question-i18"
i18_q.title = '(I18) What is your main language?'
# TODO: Decide on Question Types and Answer Types
i18_q.type = "General"

i18_r1 = Answer()
i18_r1.id = "answer1-i18"
i18_r1.type = "Radio"
i18_r1.code = "i18_a"
i18_r1.options = [
    # @TODO Route to question 20
    {
        "value": "english",
        "label": "English"
    },
    {
        "value": "other",
        "label": "Other"
    }
]

i18_r2 = Answer()
i18_r2.id = "answer2-i18"
i18_r2.type = "Textfield"
i18_r2.code = "i18_b"
i18_r2.options = []

i18_q.add_answer(i18_r1)
i18_q.add_answer(i18_r2)
i18_s.add_question(i18_q)
page8.add_section(i18_s)
test_questionnaire.register(i18_s)
test_questionnaire.register(i18_q)
test_questionnaire.register(i18_r1)
test_questionnaire.register(i18_r2)


# I19
i19_s = Section()
i19_s.id = 'section-i19'

i19_q = Question()
i19_q.id = 'question-i19'
i19_q.title = "(I19) How well can you speak English?"
i19_q.type = "General"

i19_r = Answer()
i19_r.id = 'answer-i19'
i19_r.type = "Radio"
i19_r.code = 'I19'
i19_r.options = [
    {
        "value": "i19_a",
        "label": "Very Well"
    },
    {
        "value": "i19_b",
        "label": "Well"
    },
    {
        "value": "i19_c",
        "label": "Not well"
    },
    {
        "value": "i19_d",
        "label": "Not at all"
    }
]

i19_q.add_answer(i19_r)
i19_s.add_question(i19_q)
page8.add_section(i19_s)
test_questionnaire.register(i19_s)
test_questionnaire.register(i19_q)
test_questionnaire.register(i19_r)

# I20
i20_s = Section()
i20_s.id = 'section-i20'

i20_q = Question()
i20_q.id = 'question-i20'
i20_q.title = "(I20) What is your religion?"
i20_q.description = "This question is voluntary"
i20_q.type = "General"

i20_r1 = Answer()
i20_r1.id = 'answer-i20'
i20_r1.type = "Checkbox"
i20_r1.code = 'I20'
i20_r1.label = "White"
i20_r1.options = [
    {
        "value": "i20_a",
        "label": "No religion"
    },
    {
        "value": "i20_b",
        "label": "Christian (include Church of England, Catholic, Protestant and all other Christian denominations)"
    },
    {
        "value": "i20_c",
        "label": "Buddhist"
    },
    {
        "value": "i20_d",
        "label": "Hindu"
    },
    {
        "value": "i20_e",
        "label": "Jewish"
    },
    {
        "value": "i20_f",
        "label": "Muslim"
    },
    {
        "value": "i20_g",
        "label": "Sikh"
    },
    {
        "value": "i20_h",
        "label": "Any other religion, write in"
    }
]

i20_r2 = Answer()
i20_r2.id = 'answer-i20-other'
i20_r2.type = 'textfield'
i20_r2.code = "I16"

i20_q.add_answer(i20_r1)
i20_q.add_answer(i20_r2)
i20_s.add_question(i20_q)
page8.add_section(i20_s)
test_questionnaire.register(i20_s)
test_questionnaire.register(i20_q)
test_questionnaire.register(i20_r1)
test_questionnaire.register(i20_r2)
