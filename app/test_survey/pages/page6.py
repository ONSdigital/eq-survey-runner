from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response

from app.test_survey.test_survey import test_questionnaire

page6 = Block()
page6.id = 'page-6'
page6.title = "Household questions"
test_questionnaire.register(page6)

# H7
h7_s = Section()
h7_s.id = "section-h7"

h7_q = Question()
h7_q.id = "question-h7"
h7_q.title = '(H7) What type of accommodation is this?'
# TODO: Decide on Question Types and Response Types
h7_q.type = "Checkboxes"

h7_r1 = Response()
h7_r1.id = "response1-h7"
h7_r1.type = "Checkbox"
h7_r1.label = "A whole house or bungalow that is:"
h7_r1.code = "H7"
h7_r1.options = [
    {
        "value": "h7_a",
        "label": "Detached"
    },
    {
        "value": "h7_b",
        "label": "semi-detached"
    },
    {
        "value": "h7_c",
        "label": "terraced (including end-terrace)"
    },
]

h7_r2 = Response()
h7_r2.id = "response2-h7"
h7_r2.type = "Checkbox"
h7_r2.label = "A flat, maisonette or apartment that is:"
h7_r2.code = "H7"
h7_r2.options = [
    {
        "value": "h7_d",
        "label": "in a purpose-built block of flats or tenement"
    },
    {
        "value": "h7_e",
        "label": "part of a converted or shared house (including bedsits)"
    },
    {
        "value": "h7_f",
        "label": "in a commercial building (for example, in an office building, hotel, or over a shop)"
    },
]

h7_r3 = Response()
h7_r3.id = "response3-h7"
h7_r3.type = "Checkbox"
h7_r3.label = "A mobile or temporary structure:"
h7_r3.code = "H7"
h7_r3.options = [
    {
        "value": "h7_g",
        "label": "a caravan or other mobile or temporary structure"
    }
]


h7_q.add_response(h7_r1)
h7_q.add_response(h7_r2)
h7_q.add_response(h7_r3)
h7_s.add_question(h7_q)
page6.add_section(h7_s)
test_questionnaire.register(h7_s)
test_questionnaire.register(h7_q)
test_questionnaire.register(h7_r1)
test_questionnaire.register(h7_r2)
test_questionnaire.register(h7_r3)


# H8
h8_s = Section()
h8_s.id = 'section-h8'

h8_q = Question()
h8_q.id = 'question-h8'
h8_q.title = "(H8) Is this household's accommodation self-contained?"
h8_q.description = ''
h8_q.type = "Radio"

h8_r = Response()
h8_r.id = 'response-h8'
h8_r.type = "Radio"
h8_r.code = 'H2'
h8_r.options = [
    {
        "value": "h8_a",
        "label": "Yes, all the rooms are behind a door that only this household can use"
    },
    {
        "value": "h8_b",
        "label": "No"
    }
]
h8_r.guidance = "This means that all the rooms, including the kitchen, bathroom and toilet, are behind a door that only this household can use"  # NOQA

h8_q.add_response(h8_r)
h8_s.add_question(h8_q)
page6.add_section(h8_s)
test_questionnaire.register(h8_s)
test_questionnaire.register(h8_q)
test_questionnaire.register(h8_r)

# H3
# @TODO: Write H3

# H9
h9_s = Section()
h9_s.id = 'section-h9'

h9_q = Question()
h9_q.id = 'question-h9'
h9_q.title = '(H9) How many rooms are available for use only by this household?'  # NOQA
h9_q.description = ''
h9_q.type = "General"


h9_r = Response()
h9_r.type = "Integer"
h9_r.code = 'H9'
h9_r.id = "response-h9"
h9_r.label = "Number of rooms"
h9_r.guidance = '<p>Do NOT count</p><ul><li>bathrooms</li><li>toilets</li><li>halls or landings</li><li>rooms that can only be used for storage such as cupboards</li></ul><p>Count all other rooms, for example:</p><ul><li>kitchens</li><li>liviing rooms</li><li>utility rooms</li><li>bedrooms</li><li>studies</li><li>conservatories</li></ul><p> if two rooms have been converted into one, count them as one</p>'  # NOQA

h9_q.add_response(h9_r)
h9_s.add_question(h9_q)
page6.add_section(h9_s)
test_questionnaire.register(h9_s)
test_questionnaire.register(h9_q)
test_questionnaire.register(h9_r)

# H10
h10_s = Section()
h10_s.id = 'section-h10'

h10_q = Question()
h10_q.id = 'question-h10'
h10_q.title = '(H10) How many of these rooms are bedrooms?'
h10_q.description = ''
h10_q.type = "Integer"

h10_r = Response()
h10_r.id = 'response-h10'
h10_r.type = "PositiveInteger"
h10_r.code = 'H10'
h10_r.label = "Number of bedrooms"
h10_r.guidance = 'Include all rooms built or converted for use as bedrooms, even if they are not currently used as bedrooms'  # NOQA

h10_q.add_response(h10_r)
h10_s.add_question(h10_q)
page6.add_section(h10_s)
test_questionnaire.register(h10_s)
test_questionnaire.register(h10_q)
test_questionnaire.register(h10_r)


# H11
h11_s = Section()
h11_s.id = "section-h11"

h11_q = Question()
h11_q.id = "question-h11"
h11_q.title = '(H11) What type of central heating does this accomodation have?'
h11_q.description = '<p>Tick all that apply, whether or not you use it</p>'
# TODO: Decide on Question Types and Response Types
h11_q.type = "Checkboxes"

h11_r = Response()
h11_r.id = "response1-h11"
h11_r.type = "Checkbox"
h11_r.code = "H11"
h11_r.guidance = "<p>Central heating is a central system that generates heat for multiple rooms<p>"
h11_r.options = [
    {
        "value": "h11_a",
        "label": "No central heating"
    },
    {
        "value": "h11_b",
        "label": "Gas"
    },
    {
        "value": "h11_c",
        "label": "Electric (including storage heaters)"
    },
    {
        "value": "h11_d",
        "label": "Oil"
    },
    {
        "value": "h11_e",
        "label": "Solid fuel (for example wood, coal)"
    },
    {
        "value": "h11_f",
        "label": "Other central heating"
    }
]


h11_q.add_response(h11_r)
h11_s.add_question(h11_q)
page6.add_section(h11_s)
test_questionnaire.register(h11_s)
test_questionnaire.register(h11_q)
test_questionnaire.register(h11_r)

# H12
h12_s = Section()
h12_s.id = "section-h12"

h12_q = Question()
h12_q.id = "question-h12"
h12_q.title = '(H12) Does your household own or rent this accomodation?'
h12_q.description = '<p>Select one box only<p>'
# TODO: Decide on Question Types and Response Types
h12_q.type = "Radio"

h12_r = Response()
h12_r.id = "response1-h12"
h12_r.type = "Radio"
h12_r.code = "H12"
h12_r.options = [
    # TODO: This option should route to question H14
    {
        "value": "h12_a",
        "label": "Owns outright"
    },
    # TODO: This option should route to question H14
    {
        "value": "h12_b",
        "label": "Owns with a mortgage or loan"
    },
    {
        "value": "h12_c",
        "label": "Part owns and part rent (shared ownership)"
    },
    {
        "value": "h12_d",
        "label": "Rents (with or without housing benefit)"
    },
    {
        "value": "h12_e",
        "label": "Lives here rent free"
    }
]


h12_q.add_response(h12_r)
h12_s.add_question(h12_q)
page6.add_section(h12_s)
test_questionnaire.register(h12_s)
test_questionnaire.register(h12_q)
test_questionnaire.register(h12_r)

# H13
h13_s = Section()
h13_s.id = "section-h13"

h13_q = Question()
h13_q.id = "question-h13"
h13_q.title = '(H13) Who is your landlord?'
h13_q.description = '<p>Select one box only<p>'
# TODO: Decide on Question Types and Response Types
h13_q.type = "Radio"

h13_r = Response()
h13_r.id = "response1-h13"
h13_r.type = "Radio"
h13_r.code = "H13"
h13_r.options = [
    {
        "value": "h13_a",
        "label": "Housing association, housing co-operative, charitable trust, registered social landlord"
    },
    {
        "value": "h13_b",
        "label": "Council (local authority)"
    },
    {
        "value": "h13_c",
        "label": "Private landlord or letting agency"
    },
    {
        "value": "h13_d",
        "label": "Employer of a household member"
    },
    {
        "value": "h13_e",
        "label": "Relative or friend of a household member"
    },
    {
        "value": "h13_f",
        "label": "Other"
    }
]


h13_q.add_response(h13_r)
h13_s.add_question(h13_q)
page6.add_section(h13_s)
test_questionnaire.register(h13_s)
test_questionnaire.register(h13_q)
test_questionnaire.register(h13_r)

# H14
h14_s = Section()
h14_s.id = "section-h14"

h14_q = Question()
h14_q.id = "question-h14"
h14_q.title = '(H14) In total, how many cars or vans are owned, or available for use, by members of this household?'
h14_q.description = '<p>Include any company car(s) or van(s) available for private use<p>'
# TODO: Decide on Question Types and Response Types
h14_q.type = "Radios"

h14_r1 = Response()
h14_r1.id = "response1-h14"
h14_r1.type = "Radio"
h14_r1.code = "H14"
h14_r1.options = [
    {
        "value": "h14_a",
        "label": "None"
    },
    {
        "value": "h14_b",
        "label": "1"
    },
    {
        "value": "h14_c",
        "label": "2"
    },
    {
        "value": "h14_d",
        "label": "3"
    },
    {
        "value": "h14_e",
        "label": "4 or more, write in number"
    }
]

h14_r2 = Response()
h14_r2.id = 'response2-h14'
h14_r2.type = 'positiveinteger'
h14_r2.code = "H14"

h14_q.add_response(h14_r1)
h14_q.add_response(h14_r2)
h14_s.add_question(h14_q)
page6.add_section(h14_s)
test_questionnaire.register(h14_s)
test_questionnaire.register(h14_q)
test_questionnaire.register(h14_r1)
test_questionnaire.register(h14_r2)
