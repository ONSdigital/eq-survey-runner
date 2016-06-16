from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response

from app.surveys.large_test import test_questionnaire

page3 = Block()
page3.id = 'page-3'
page3.title = "Household questions"
test_questionnaire.register(page3)

# H1
h1_s = Section()
h1_s.id = "section-h1"

h1_q = Question()
h1_q.id = "question-h1"
h1_q.title = '(H1) Who usually lives here?'
h1_q.description = 'Select all that apply'
# TODO: Decide on Question Types and Response Types
h1_q.type = "Checkboxes"

h1_r = Response()
h1_r.id = "response-h1"
h1_r.type = "Checkbox"
h1_r.code = "H1"
h1_r.options = [
    {
        "value": "h1_a",
        "label": "Me, this is my permanent or family home"
    },
    {
        "value": "h1_b",
        "label": "Family members including partners, children, and babies born on or before 27 March 2011"
    },
    {
        "value": "h1_c",
        "label": "Students and/or schoolchildren who live away from home during term time"
    },
    {
        "value": "h1_d",
        "label": "Housemates, tenants or lodgers"
    },
    {
        "value": "h1_e",
        "label": "People who usually live outside the UK who are staying in the UK for 3 months or more"
    },
    {
        "value": "h1_f",
        "label": "People who work away from home within the UK, or are members of the armed forces, if this is their permanent or family home"
    },
    {
        "value": "h1_g",
        "label": "People staying temporarily outside the UK for less than 12 months"
    },
    {
        "value": "h1_h",
        "label": "People staying temporarily who usually live in the UK but do not have another UK address, for example, relatives, friends"
    },
    {
        "value": "h1_i",
        "label": "Other people who usually live here, including anyone temporarily away from home"
    },

    # TODO: This option should be exclusive and unset other options
    # TODO: This option should route the respondent to H4
    {
        "value": "h1_j",
        "label": "No-one usually lives here, for example, this is a second address or holiday home"
    }
]

h1_q.add_response(h1_r)
h1_s.add_question(h1_q)
page3.add_section(h1_s)
test_questionnaire.register(h1_s)
test_questionnaire.register(h1_q)
test_questionnaire.register(h1_r)


# H2
h2_s = Section()
h2_s.id = 'section-h2'

h2_q = Question()
h2_q.id = 'question-h2'
h2_q.title = '(H2) Counting everyone you included in question H1, how many people usually live here?'
h2_q.type = "Integer"

h2_r = Response()
h2_r.type = "PositiveInteger"
h2_r.code = 'H2'
h2_r.id = 'response-h2'

h2_q.add_response(h2_r)
h2_s.add_question(h2_q)
page3.add_section(h2_s)
test_questionnaire.register(h2_s)
test_questionnaire.register(h2_q)
test_questionnaire.register(h2_r)

# H3
# @TODO: Write H3

# H4
h4_s = Section()
h4_s.id = 'section-h4'

h4_q = Question()
h4_q.id = 'question-h4'
h4_q.title = '(H4) Apart from everyone counted in question H2, who else is staying overnight here on {exercise.return_by:%-d %B %Y}? These people are counted as visitors. Remember to include children and babies.'  # NOQA
h4_q.description = 'Tick all that apply'
h4_q.type = "Checkboxes"


h4_r = Response()
h4_r.type = "Checkbox"
h4_r.code = 'H4'
h4_r.id = "response-h4"
h4_r.options = [
    {
        "value": "h4_a",
        "label": "People who usually live somewhere else in the UK, for example, boy/girlfriends, friends, relatives"
    },
    {
        "value": "h4_b",
        "label": "People staying here because it is their second address, for example, for work. Their permanent or family home is elsewhere"
    },
    {
        "value": "h4_c",
        "label": "People who usually live outside the UK who are staying in the UK for less than 3 months"
    },
    {
        "value": "h4_d",
        "label": "People here on holiday"
    },

    # TODO: This option should be exclusive and unset other options
    # TODO: This option should route the respondent to H6
    {
        "value": "h4_e",
        "label": "There are no visitors staying overnight here on {exercise.return_by:%-d %B %Y}"
    }
]

h4_q.add_response(h4_r)
h4_s.add_question(h4_q)
page3.add_section(h4_s)
test_questionnaire.register(h4_s)
test_questionnaire.register(h4_q)
test_questionnaire.register(h4_r)

# H5
h5_s = Section()
h5_s.id = 'section-h5'

h5_q = Question()
h5_q.id = 'question-h5'
h5_q.title = '(H5) Counting only the people included in question H4, how many visitors are staying overnight here on {exercise.return_by:%-d %B %Y}?'
h5_q.description = 'If there is no-one usually living here (there are only visitors staying here) answer questions H7 to H11 on page 6 and then go to the back page (page 32) to answer the Visitor questions'  # NOQA
h5_q.type = "Integer"

h5_r = Response()
h5_r.id = "response-h5"
h5_r.type = "PositiveInteger"
h5_r.code = 'H5'

h5_q.add_response(h5_r)
h5_s.add_question(h5_q)
page3.add_section(h5_s)
test_questionnaire.register(h5_s)
test_questionnaire.register(h5_q)
test_questionnaire.register(h5_r)
