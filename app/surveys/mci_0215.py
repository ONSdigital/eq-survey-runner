import copy
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response
from app.surveys.mci_0205 import mci_0205
from app.validation.abstract_validator import AbstractValidator


# The 0203 Form is the same as 0205 but without the fuel question
# Copy the survey first by exporting and then reimporting
mci_0215 = copy.deepcopy(mci_0205)
group = mci_0215.get_item_by_id("14ba4707-321d-441d-8d21-b8367366e766")

questionnaire = mci_0215
eq_id = "1"
form_type = "0215"

# Create block 2
b2 = Block()
b2.id = "2d24cb72-5598-4c3e-bd53-1d21bb12455f"
b2.title = "Monthly Business Survey"

group.add_block(b2)
questionnaire.register(b2)

# Add the sections

###
# Section Four
###

s4 = Section()
s4.id = "c528d24b-d0dd-45cd-91af-380b61a5725d"
s4.title = "On {exercise.employment_date:%-d %B %Y} what was the number of employees for the business?"
s4.description = "<p>An employee is anyone aged 16 years or over that your organisation directly pays from its payroll(s), in return for carrying out a full-time or part-time job or being on a training scheme.</p><div> <h4>Include</h4> <ul> <li>all workers paid directly from this business’s payroll(s)</li> <li>those temporarily absent but still being paid, for example on maternity leave</li></ul> </div> <div> <h4>Exclude</h4> <ul> <li>agency workers paid directly from the agency payroll</li><li>voluntary workers</li><li>former employees only receiving pension</li><li>self-employed workers</li><li><u>working</u> owners who are not paid via PAYE</li></ul> </div>"  # NOQA
b2.add_section(s4)
questionnaire.register(s4)


q11 = Question()
q11.id = "59ccb6e3-4a0a-4c32-b798-aafbf6b9e481"
q11.title = ""
q11.description = ""
q11.type = "Integer"

s4.add_question(q11)
questionnaire.register(q11)

q11r = Response()
q11r.id = "cffbbca5-1162-44d8-bbfb-3bc733d80239"
q11r.code = "51"
q11r.label = "What was the number of male employees working more than 30 hours per week?"
q11r.guidance = ""
q11r.type = "Integer"
q11r.options = []
q11r.mandatory = False
q11r.messages = {
    "NOT_INTEGER": "Please only enter whole numbers into the field.",
    "NEGATIVE_INTEGER": "The value cannot be negative. Please correct your answer.",
    "INTEGER_TOO_LARGE": "The maximum value allowed is 9999999999. Please correct your answer."
}

q11.add_response(q11r)
questionnaire.register(q11r)

q12 = Question()
q12.id = "fdafbc19-25b0-4985-a676-100df5bf25d3"
q12.title = ""
q12.description = ""
q12.type = "Integer"

s4.add_question(q12)
questionnaire.register(q12)

q12r = Response()
q12r.id = "c5908b75-d63d-4518-b00e-a60919aa63cd"
q12r.code = "52"
q12r.label = "What was the number of male employees working 30 hours or less per week?"
q12r.guidance = ""
q12r.type = "Integer"
q12r.options = []
q12r.mandatory = False
q12r.messages = {
    "NOT_INTEGER": "Please only enter whole numbers into the field.",
    "NEGATIVE_INTEGER": "The value cannot be negative. Please correct your answer.",
    "INTEGER_TOO_LARGE": "The maximum value allowed is 9999999999. Please correct your answer."
}

q12.add_response(q12r)
questionnaire.register(q12r)

q13 = Question()
q13.id = "e10d5a63-ac30-4031-8c71-20eb04196978"
q13.title = ""
q13.description = ""
q13.type = "Integer"

s4.add_question(q13)
questionnaire.register(q13)

q13r = Response()
q13r.id = "0ac86568-2e33-420c-9dfe-f47a95132a5a"
q13r.code = "53"
q13r.label = "What was the number of female employees working more than 30 hours per week?"
q13r.guidance = ""
q13r.type = "Integer"
q13r.options = []
q13r.mandatory = False
q13r.messages = {
    "NOT_INTEGER": "Please only enter whole numbers into the field.",
    "NEGATIVE_INTEGER": "The value cannot be negative. Please correct your answer.",
    "INTEGER_TOO_LARGE": "The maximum value allowed is 9999999999. Please correct your answer."
}

q13.add_response(q13r)
questionnaire.register(q13r)

q14 = Question()
q14.id = "87f52d2a-b0e4-47f2-b884-ce94df109ed9"
q14.title = ""
q14.description = ""
q14.type = "Integer"

s4.add_question(q14)
questionnaire.register(q14)

q14r = Response()
q14r.id = "ed675602-9696-49ba-b3b9-2ea582ffe171"
q14r.code = "54"
q14r.label = "What was the number of female employees working 30 hours or less per week?"
q14r.guidance = ""
q14r.type = "Integer"
q14r.options = []
q14r.mandatory = False
q14r.messages = {
    "NOT_INTEGER": "Please only enter whole numbers into the field.",
    "NEGATIVE_INTEGER": "The value cannot be negative. Please correct your answer.",
    "INTEGER_TOO_LARGE": "The maximum value allowed is 9999999999. Please correct your answer."
}

q14.add_response(q14r)
questionnaire.register(q14r)

q15 = Question()
q15.id = "b08ffc0f-c148-462e-a988-0a8ca259436a"
q15.title = ""
q15.description = ""
q15.type = "Integer"

s4.add_question(q15)
questionnaire.register(q15)

q15r = Response()
q15r.id = "42ee21a7-c050-49f7-9cdc-647596f22317"
q15r.code = "50"
q15r.label = "What was the number of total employees?"
q15r.guidance = ""
q15r.type = "Integer"
q15r.options = []
q15r.mandatory = True
q15r.messages = {
    AbstractValidator.MANDATORY: "Please provide a value, even if your value is 0.",
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q15.add_response(q15r)
questionnaire.register(q15r)
