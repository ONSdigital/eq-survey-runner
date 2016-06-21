from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response

from app.surveys.large_test import test_questionnaire

page7 = Block()
page7.id = 'page-7'
page7.title = "Individual questions"
test_questionnaire.register(page7)

# I1
i1_s = Section()
i1_s.id = "section-i1"

i1_q = Question()
i1_q.id = "question-i1"
i1_q.title = '(I1) What is your name?'
# TODO: Decide on Question Types and Response Types
i1_q.type = "General"

i1_r1 = Response()
i1_r1.id = "response1-i1"
i1_r1.type = "Textfield"
i1_r1.label = "First name:"
i1_r1.code = "i1_a"
i1_r1.options = []

i1_r2 = Response()
i1_r2.id = "response2-i1"
i1_r2.type = "Textfield"
i1_r2.label = "Last name:"
i1_r2.code = "i1_b"
i1_r2.options = []

i1_q.add_response(i1_r1)
i1_q.add_response(i1_r2)
i1_s.add_question(i1_q)
page7.add_section(i1_s)
test_questionnaire.register(i1_s)
test_questionnaire.register(i1_q)
test_questionnaire.register(i1_r1)
test_questionnaire.register(i1_r2)


# I2
i2_s = Section()
i2_s.id = 'section-i2'

i2_q = Question()
i2_q.id = 'question-i2'
i2_q.title = "(I2) What is your sex?"
i2_q.type = "General"

i2_r = Response()
i2_r.id = 'response-i2'
i2_r.type = "Radio"
i2_r.code = 'I2'
i2_r.options = [
    {
        "value": "Male",
        "label": "Male"
    },
    {
        "value": "Female",
        "label": "Female"
    }
]

i2_q.add_response(i2_r)
i2_s.add_question(i2_q)
page7.add_section(i2_s)
test_questionnaire.register(i2_s)
test_questionnaire.register(i2_q)
test_questionnaire.register(i2_r)

# I3
i3_s = Section()
i3_s.id = 'section-i3'

i3_q = Question()
i3_q.id = 'question-i3'
i3_q.title = "(I3) What is your date of birth?"
i3_q.type = "General"

i3_r = Response()
i3_r.id = 'response-i3'
i3_r.type = "Date"
i3_r.code = "I3"

i3_q.add_response(i3_r)
i3_s.add_question(i3_q)
page7.add_section(i3_s)
test_questionnaire.register(i3_r)
test_questionnaire.register(i3_q)
test_questionnaire.register(i3_s)

# I4
i4_s = Section()
i4_s.id = "section-i4"

i4_q = Question()
i4_q.id = "question-i4"
i4_q.title = '(I4) On {exercise.return_by:%-d %B %Y}, what is your legal marital or same-sex civil partnership status?'
i4_q.type = "General"

i4_r = Response()
i4_r.id = "response1-i4"
i4_r.type = "Radio"
i4_r.code = "I4"
i4_r.options = [
    {
        "value": "i4_a",
        "label": "Never married and never registered a same-sex civil partnership"
    },
    {
        "value": "i4_b",
        "label": "Married"
    },
    {
        "value": "i4_c",
        "label": "In a registered same-sex civil partnership"
    },
    {
        "value": "i4_d",
        "label": "Separated, but still legally married"
    },
    {
        "value": "i4_e",
        "label": "Separated, but still in a same-sex civil partnership"
    },
    {
        "value": "i4_f",
        "label": "Divorced"
    },
    {
        "value": "i4_g",
        "label": "Formerly in a same-sex civil partnership which is now legally dissolved"
    },
    {
        "value": "i4_h",
        "label": "Widowed"
    },
    {
        "value": "i4_i",
        "label": "Surviving partner from a same-sex civil partnership"
    }
]


i4_q.add_response(i4_r)
i4_s.add_question(i4_q)
page7.add_section(i4_s)
test_questionnaire.register(i4_s)
test_questionnaire.register(i4_q)
test_questionnaire.register(i4_r)

# @TODO Implement I5

# I6
i6_s = Section()
i6_s.id = "section-i6"

i6_q = Question()
i6_q.id = "question-i6"
i6_q.title = '(I6) What is that address?'
# TODO: Decide on Question Types and Response Types
i6_q.type = "General"

i6_r = Response()
i6_r.id = "response1-i6"
i6_r.type = "Radio"
i6_r.code = "I6"
i6_r.options = [
    {
        "value": "i6_a",
        "label": "Armed force base address"
    },
    {
        "value": "i6_b",
        "label": "Another address when working away from home"
    },
    {
        "value": "i6_c",
        "label": "Student's home address"
    },
    {
        "value": "i6_d",
        "label": "Student's term time address"
    },
    {
        "value": "i6_e",
        "label": "Another parents or guardians's address"
    },
    {
        "value": "i6_f",
        "label": "Holiday home"
    },
    {
        "value": "i6_g",
        "label": "Other"
    }
]


i6_q.add_response(i6_r)
i6_s.add_question(i6_q)
page7.add_section(i6_s)
test_questionnaire.register(i6_s)
test_questionnaire.register(i6_q)
test_questionnaire.register(i6_r)

# I7
i7_s = Section()
i7_s.id = 'section-i7'

i7_q = Question()
i7_q.id = 'question-i7'
i7_q.title = "(I7) Are you a schoolchild or student in full-time education?"
i7_q.type = "General"

i7_r = Response()
i7_r.id = 'response-i7'
i7_r.type = "Radio"
i7_r.code = 'I7'
i7_r.options = [
    {
        "value": "Yes",
        "label": "Yes"
    },
    # @TODO: Should route to question i()
    {
        "value": "No",
        "label": "No"
    }
]

i7_q.add_response(i7_r)
i7_s.add_question(i7_q)
page7.add_section(i7_s)
test_questionnaire.register(i7_s)
test_questionnaire.register(i7_q)
test_questionnaire.register(i7_r)

# I8
i8_s = Section()
i8_s.id = "section-i8"

i8_q = Question()
i8_q.id = "question-i8"
i8_q.title = '(I8) During term time, do you live:'
# TODO: Decide on Question Types and Response Types
i8_q.type = "General"

i8_r = Response()
i8_r.id = "response1-i8"
i8_r.type = "Radio"
i8_r.code = "I8"
i8_r.options = [
    {
        "value": "i8_a",
        "label": "At the address on the front of this questionnaire?"
    },
    # @TODO: Should route to question 43
    {
        "value": "i8_b",
        "label": "At the address in question 5?"
    },
    # @TODO: Should route to question 43
    {
        "value": "i8_c",
        "label": "At another address?"
    }
]

i8_q.add_response(i8_r)
i8_s.add_question(i8_q)
page7.add_section(i8_s)
test_questionnaire.register(i8_s)
test_questionnaire.register(i8_q)
test_questionnaire.register(i8_r)

# I9
i9_s = Section()
i9_s.id = "section-i9"

i9_q = Question()
i9_q.id = "question-i9"
i9_q.title = '(I9) What is your country of birth?'
# TODO: Decide on Question Types and Response Types
i9_q.type = "General"

i9_r1 = Response()
i9_r1.id = "response1-i9"
i9_r1.type = "Radio"
i9_r1.code = "I9"
i9_r1.options = [
    # @TODO: Should route to question 13
    {
        "value": "i9_a",
        "label": "England"
    },
    # @TODO: Should route to question 13
    {
        "value": "i9_b",
        "label": "Wales"
    },
    # @TODO: Should route to question 13
    {
        "value": "i9_c",
        "label": "Scotland"
    },
    # @TODO: Should route to question 13
    {
        "value": "i9_d",
        "label": "Northern Ireland"
    },
    {
        "value": "i9_e",
        "label": "Republic of Ireland"
    },
    {
        "value": "i9_f",
        "label": "Elsewhere"
    }
]

i9_r2 = Response()
i9_r2.id = 'response2-i9'
i9_r2.type = 'textfield'
i9_r2.code = "H14"

i9_q.add_response(i9_r1)
i9_q.add_response(i9_r2)
i9_s.add_question(i9_q)
page7.add_section(i9_s)
test_questionnaire.register(i9_s)
test_questionnaire.register(i9_q)
test_questionnaire.register(i9_r1)
test_questionnaire.register(i9_r2)

# I10
i10_s = Section()
i10_s.id = 'section-i10'

i10_q = Question()
i10_q.id = 'question-i10'
i10_q.title = "(I10) If you were not born in the united kingdom, when did you most recently arrive to live here?"
i10_q.description = "Do not count short stay visits away from the UK"
i10_q.type = "General"

# @TODO: Should show month and year only
i10_r = Response()
i10_r.id = 'response-i10'
i10_r.type = "Date"
i10_r.code = "I10"

i10_q.add_response(i10_r)
i10_s.add_question(i10_q)
test_questionnaire.register(i10_r)
test_questionnaire.register(i10_q)
test_questionnaire.register(i10_s)

# @TODO: Question 11 is a simple routing check which directs the user based on the date entered in i10
i11_s = Section()
i11_s.id = 'section-i11'

i11_q = Question()
i11_q.id = 'question-i11'
i11_q.title = "This question on the paper form just contains a routing instruction.  Here it is used to test whether we can display simple instructions"
i11_q.type = "General"

i11_s.add_question(i11_q)
page7.add_section(i11_s)
test_questionnaire.register(i11_s)
test_questionnaire.register(i11_q)

# I12
i12_s = Section()
i12_s.id = "section-i12"

i12_q = Question()
i12_q.id = "question-i12"
i12_q.title = '(I12) Including the time you have already spent here, how long do you intend to stay in the United Kingdom?'
# TODO: Decide on Question Types and Response Types
i12_q.type = "General"

i12_r = Response()
i12_r.id = "response1-i12"
i12_r.type = "Radio"
i12_r.code = "I12"
i12_r.options = [
    {
        "value": "i12_a",
        "label": "Less than 6 months"
    },
    {
        "value": "i12_b",
        "label": "6 months or more but less than 12 months"
    },
    {
        "value": "i12_c",
        "label": "12 months or more"
    }
]

i12_q.add_response(i12_r)
i12_s.add_question(i12_q)
page7.add_section(i12_s)
test_questionnaire.register(i12_s)
test_questionnaire.register(i12_q)
test_questionnaire.register(i12_r)

# I13
i13_s = Section()
i13_s.id = "section-i13"

i13_q = Question()
i13_q.id = "question-i13"
i13_q.title = '(I13) How is your health in general?'
# TODO: Decide on Question Types and Response Types
i13_q.type = "General"

i13_r = Response()
i13_r.id = "response1-i13"
i13_r.type = "Radio"
i13_r.code = "I13"
i13_r.options = [
    {
        "value": "i13_a",
        "label": "Very good"
    },
    {
        "value": "i13_b",
        "label": "Good"
    },
    {
        "value": "i13_c",
        "label": "Fair"
    },
    {
        "value": "i13_d",
        "label": "Bad"
    },
    {
        "value": "i13_d",
        "label": "Very Bad"
    }
]

i13_q.add_response(i13_r)
i13_s.add_question(i13_q)
page7.add_section(i13_s)
test_questionnaire.register(i13_s)
test_questionnaire.register(i13_q)
test_questionnaire.register(i13_r)

# I14
i14_s = Section()
i14_s.id = "section-i14"

i14_q = Question()
i14_q.id = "question-i14"
i14_q.title = '(I14) Do you look after, or give any help or support to family members, friends, neighbours or others because of either: long-term physical or mental ill-health/disability?; problems related to old age?'  # NOQA
i14_q.description = "Do not count anything you do as part of your paid employment"
# TODO: Decide on Question Types and Response Types
i14_q.type = "General"

i14_r = Response()
i14_r.id = "response1-i14"
i14_r.type = "Radio"
i14_r.code = "I14"
i14_r.options = [
    {
        "value": "i14_a",
        "label": "No"
    },
    {
        "value": "i14_b",
        "label": "Yes, 1 - 19 Hours a week"
    },
    {
        "value": "i14_c",
        "label": "Yes, 20 - 49 Hours a week"
    },
    {
        "value": "i14_d",
        "label": "Yes, 50 or more hours a week"
    }
]

i14_q.add_response(i14_r)
i14_s.add_question(i14_q)
page7.add_section(i14_s)
test_questionnaire.register(i14_s)
test_questionnaire.register(i14_q)
test_questionnaire.register(i14_r)
