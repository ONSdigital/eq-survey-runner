from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.answer import Answer
from app.model.display import Display
from app.model.introduction import Introduction
from app.validation.abstract_validator import AbstractValidator


# Create the questionnaire object
star_wars = Questionnaire()
questionnaire = star_wars
questionnaire.eq_id = "0"
form_type = "star_wars"

questionnaire.id = "0"
questionnaire.title = "Star Wars"

# Currently not used on the frontend
questionnaire.description = "Kitchen sink test for the Star Wars questionnaire"
questionnaire.survey_id = "0"

introduction = Introduction()
introduction.description = "May the force be with you"
questionnaire.introduction = introduction

group = Group()
group.id = "14ba4707-321d-441d-8d21-b8367366e766"
group.title = ""

questionnaire.add_group(group)
questionnaire.register(group)

b1 = Block()
b1.id = "cd3b74d1-b687-4051-9634-a8f9ce10a27d"
b1.title = "Star Wars"

group.add_block(b1)
questionnaire.register(b1)

# Add the sections

###
# Section One
###

s1 = Section()
s1.id = "017880bc-752d-4a6b-83df-e130409ee660"
s1.title = "Star Wars Quiz"
s1.description = "May the force be with you young EQ developer<br/><br/>"

b1.add_section(s1)
questionnaire.register(s1)


q1 = Question()
q1.id = "88824eff-7bb6-443f-85cb-8c2db016d44c"
q1.title = ""
q1.description = ""
q1.type = "Integer"

s1.add_question(q1)
questionnaire.register(q1)

q1r = Answer()
q1r.id = "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b"
q1r.code = "1"
q1r.label = "How old is Chewy?"
q1r.guidance = ""
q1r.type = "Integer"
q1r.options = []
q1r.mandatory = True
q1r.messages = {
    AbstractValidator.NOT_INTEGER: "Please enter your age.",
    AbstractValidator.NEGATIVE_INTEGER: "Negative age you can not be.",
    AbstractValidator.INTEGER_TOO_LARGE: "No one lives that long, not even Yoda"
}

q1.add_answer(q1r)
questionnaire.register(q1r)

q2 = Question()
q2.id = "b8a803ba-2048-46dc-83cf-9ef9000d7a92"
q2.title = ""
q2.description = ""
q2.type = "Currency"

s1.add_question(q2)
questionnaire.register(q2)

q2r = Answer()
q2r.id = "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c"
q2r.code = "2"
q2r.label = "How many Octillions do Nasa reckon it would cost to build a death star?"
q2r.guidance = ""
q2r.type = "Currency"
q2r.options = []
q2r.mandatory = True
q2r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "How can it be negative?",
    AbstractValidator.INTEGER_TOO_LARGE: "How much, idiot you must be"
}

q2.add_answer(q2r)
questionnaire.register(q2r)


q3 = Question()
q3.id = "d8a803ga-2048-46dc-83cf-9ef9000d7a92"
q3.title = ""
q3.description = ""
q3.type = "Integer"

s1.add_question(q3)
questionnaire.register(q3)

q3r = Answer()
q3r.id = "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c"
q3r.code = "3"
q3r.label = "How hot is a lightsaver in degrees C?"
q3r.guidance = ""
q3r.type = "PositiveInteger"
q3r.options = []
q3r.mandatory = False
q3r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "How can it be negative?",
    AbstractValidator.INTEGER_TOO_LARGE: "Thats hotter then the sun, Jar Jar Binks you must be"
}

q3.add_answer(q3r)
questionnaire.register(q3r)


q4 = Question()
q4.id = "235f0930-47fb-4998-afed-d73167886d63"
q4.title = "What animal was used to create the engine sound of the Empire's TIE fighters?"
q4.description = ""
q4.type = "Radios"

s1.add_question(q4)
questionnaire.register(q4)

q4r = Answer()
q4r.id = "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d"
q4r.code = "4"
q4r.label = ""
q4r.guidance = ""
q4r.type = "Radio"
q4r.options = [{
                    "value": "Lion",
                    "label": "Lion"
                }, {
                    "value": "Elephant",
                    "label": "Elephant"
                }, {
                    "value": "Cow",
                    "label": "Cow"
                }, {
                    "value": "Hippo",
                    "label": "Hippo"
                }]
q4r.mandatory = True
q4r_display = Display()
q4r_display.properties = {
    "columns": True
}
q4r.display = q4r_display

q4.add_answer(q4r)
questionnaire.register(q4r)


q5 = Question()
q5.id = "def61645-c231-4522-ba2f-273b25507e53"
q5.title = "Which of these Darth Vader quotes is wrong?"
q5.description = ""
q5.type = "Radios"

s1.add_question(q5)
questionnaire.register(q5)

q5r = Answer()
q5r.id = "7587eb9b-f24e-4dc0-ac94-66118b896c10"
q5r.code = "5"
q5r.label = ""
q5r.guidance = ""
q5r.type = "Radio"
q5r.options = [{
                    "value": "I've been waiting for you, Obi-Wan",
                    "label": "I've been waiting for you, Obi-Wan"
                }, {
                    "value": "Luke, I am your father",
                    "label": "Luke, I am your father"
                }, {
                    "value": "Together we can rule the galaxy",
                    "label": "Together we can rule the galaxy"
                }, {
                    "value": "I find your lack of faith disturbing",
                    "label": "I find your lack of faith disturbing"
                }]
q5r.mandatory = False

q5r_display = Display()
q5r_display.properties = {
    "columns": False
}
q5r.display = q5r_display

q5.add_answer(q5r)
questionnaire.register(q5r)

q6 = Question()
q6.id = "def6r645-c231-4522-ba2f-273b25507e53"
q6.title = "Which 3 have wielded a green lightsaber?"
q6.description = ""
q6.type = "Checkboxes"

s1.add_question(q6)
questionnaire.register(q6)

q6r = Answer()
q6r.id = "9587eb9b-f24e-4dc0-ac94-66117b896c10"
q6r.code = "6"
q6r.label = ""
q6r.guidance = ""
q6r.type = "Checkbox"
q6r.options = [{
                    "value": "Luke Skywalker",
                    "label": "Luke Skywalker"
                }, {
                    "value": "Yoda",
                    "label": "Yoda"
                }, {
                    "value": "Anakin Skywalker",
                    "label": "Anakin Skywalker"
                }, {
                    "value": "Rey",
                    "label": "Rey"
                }, {
                    "value": "Obi-Wan Kenobi",
                    "label": "Obi-Wan Kenobi"
                }, {
                    "value": "Qui-Gon Jinn",
                    "label": "Qui-Gon Jinn"
                }]
q6r.mandatory = True

q6r_display = Display()
q6r_display.properties = {
    "columns": True
}
q6r.display = q6r_display
q6.add_answer(q6r)
questionnaire.register(q6r)


q7 = Question()
q7.id = "pef6r645-c231-4522-ba2f-273b25507e53"
q7.title = "Which 3 appear in any of the opening crawlers?"
q7.description = ""
q7.type = "Checkboxes"

s1.add_question(q7)
questionnaire.register(q7)

q7r = Answer()
q7r.id = "5587eb9b-f24e-4dc0-ac94-66117b896c10"
q7r.code = "7"
q7r.label = ""
q7r.guidance = ""
q7r.type = "Checkbox"
q7r.options = [{
                    "value": "Luke Skywalker",
                    "label": "Luke Skywalker"
                }, {
                    "value": "Han Solo",
                    "label": "Han Solo"
                }, {
                    "value": "The Emperor",
                    "label": "The Emperor"
                }, {
                    "value": "R2D2",
                    "label": "R2D2"
                }, {
                    "value": "Senator Amidala",
                    "label": "Senator Amidala"
                }, {
                    "value": "Yoda",
                    "label": "Yoda"
                }]
q7r.mandatory = False

q7r_display = Display()
q7r_display.properties = {
    "columns": False
}
q7r.display = q7r_display
q7.add_answer(q7r)
questionnaire.register(q7r)

q8 = Question()
q8.id = "6cc86b54-330c-4465-99b2-34cc7073dc2c"
q8.title = "When was The Empire Strikes Back released?"
q8.description = "It could be between {exercise.start_date:%-d %B %Y} and {exercise.end_date:%-d %B %Y}. But that might just be a test"
q8.type = "DateRange"

s1.add_question(q8)
questionnaire.register(q8)

q8r1 = Answer()
q8r1.id = "6fd644b0-798e-4a58-a393-a438b32fe637"
q8r1.code = "81"
q8r1.label = "From"
q8r1.guidance = ""
q8r1.type = "Date"
q8r1.options = []
q8r1.mandatory = True
q8r1.messages = {
    AbstractValidator.MANDATORY: "Please answer before continuing.",
    AbstractValidator.INVALID_DATE: "The date entered is not valid.  Please correct your answer."
}

q8.add_answer(q8r1)
questionnaire.register(q8r1)

q8r2 = Answer()
q8r2.id = "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0"
q8r2.code = "82"
q8r2.label = "To"
q8r2.guidance = ""
q8r2.type = "Date"
q8r2.options = []
q8r2.mandatory = True
q8r2.messages = {
    AbstractValidator.MANDATORY: "Please answer before continuing.",
    AbstractValidator.INVALID_DATE: "The date entered is not valid.  Please correct your answer."
}

q8.add_answer(q8r2)
questionnaire.register(q8r2)

b2 = Block()
b2.id = "an3b74d1-b687-4051-9634-a8f9ce10ard"
b2.title = ""

group.add_block(b2)
questionnaire.register(b2)

s2 = Section()
s2.id = "12346782-08a6-4213-9dc9-0780c2996896"
s2.title = "On {exercise.employment_date:%-d %B %Y} how many were employed?"
s2.description = "If you didn't pick the right employment date for Return of the Jedi its your fault if this question makes no sense"

b2.add_section(s2)
questionnaire.register(s2)

q9 = Question()
q9.id = "rt4eedc2-d98c-4d4d-9a7c-997ce10c361f"
q9.title = ""
q9.description = ""
q9.type = "Integer"

s2.add_question(q9)
questionnaire.register(q9)

q9r = Answer()
q9r.id = "5rr015b1-f87c-4740-9fd4-f01f707ef558"
q9r.code = "9"
q9r.label = "What was the total number of Ewokes?"
q9r.guidance = ""
q9r.type = "Integer"
q9r.options = []
q9r.mandatory = False
q9r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "How can it be negative?",
    AbstractValidator.INTEGER_TOO_LARGE: "Thats hotter then the sun, Jar Jar Binks you must be"
}

q9.add_answer(q9r)
questionnaire.register(q9r)

s3 = Section()
s3.id = "94546782-08a6-4213-9dc9-0780c2996896"
s3.title = ""
s3.description = ""

b2.add_section(s3)
questionnaire.register(s3)

q10 = Question()
q10.id = "fef6edc2-d98c-4d4d-9a7c-997ce10c361f"
q10.title = ""
q10.description = ""
q10.type = "Textarea"

s3.add_question(q10)
questionnaire.register(q10)

q10r = Answer()
q10r.id = "215015b1-f87c-4740-9fd4-f01f707ef558"
q10r.code = "10"
q10r.label = "Why doesn't Chewbacca receive a medal at the end of A New Hope?"
q10r.guidance = ""
q10r.type = "Textarea"
q10r.options = []
q10r.mandatory = True

q10.add_answer(q10r)
questionnaire.register(q10r)

q10r_display = Display()
q10r_display.properties = {
    "max_length": "2000"
}
q10r.display = q10r_display
