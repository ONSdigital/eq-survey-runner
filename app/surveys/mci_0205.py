from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response
from app.model.display import Display
from app.model.introduction import Introduction
from app.validation.abstract_validator import AbstractValidator

# Create the questionnaire object
mci_0205 = Questionnaire()
questionnaire = mci_0205
eq_id = "1"
form_type = "0205"

questionnaire.id = "23"
questionnaire.title = "Monthly Business Survey - Retail Sales Index"
questionnaire.description = "MCI Description"
questionnaire.survey_id = "023"

introduction = Introduction()
introduction.description = "<p>The information supplied is used to produce monthly estimates of the total retail sales in Great Britain where retailing is defined as the sale of goods to the general public for household consumption. The Retail Sales Index is a key indicator of the progress of the economy. It is also used to help estimate consumer spending on retail goods and the output of the retail sector, both of which feed into the compilation of the National Accounts. The results are also used by the Bank of England and HM Treasury to inform decision making by government and in formulating financial policies. The results <a href=\"http://www.ons.gov.uk/businessindustryandtrade/retailindustry\">are published on our website</a>.</p>"  # NOQA
questionnaire.introduction = introduction

# Create the group object
group = Group()
group.id = "14ba4707-321d-441d-8d21-b8367366e766"
group.title = ""

questionnaire.add_group(group)
questionnaire.register(group)

# Create the block
b1 = Block()
b1.id = "cd3b74d1-b687-4051-9634-a8f9ce10a27d"
b1.title = "Monthly Business Survey"

group.add_block(b1)
questionnaire.register(b1)

# Add the sections

###
# Section One
###

s1 = Section()
s1.id = "f11bc7dc-3940-4c7d-9d0e-faa6acb23eeb"
s1.title = ""
s1.description = ""

b1.add_section(s1)
questionnaire.register(s1)

# Date Range question
q1 = Question()
q1.id = "6cc86b54-330c-4465-99b2-34cc7073dc2c"
q1.title = "What are the dates of the sales period you are reporting for?"
q1.description = "If possible, this should be for the period {exercise.start_date:%-d %B %Y} to {exercise.end_date:%-d %B %Y}."
q1.type = "DateRange"

s1.add_question(q1)
questionnaire.register(q1)

q1r1 = Response()
q1r1.id = "6fd644b0-798e-4a58-a393-a438b32fe637"
q1r1.code = "11"
q1r1.label = "From"
q1r1.guidance = ""
q1r1.type = "Date"
q1r1.options = []
q1r1.mandatory = True
q1r1.messages = {
    AbstractValidator.MANDATORY: "Please answer before continuing.",
    AbstractValidator.INVALID_DATE: "The date entered is not valid.  Please correct your answer."
}

q1.add_response(q1r1)
questionnaire.register(q1r1)

q1r2 = Response()
q1r2.id = "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0"
q1r2.code = "12"
q1r2.label = "To"
q1r2.guidance = ""
q1r2.type = "Date"
q1r2.options = []
q1r2.mandatory = True
q1r2.messages = {
    AbstractValidator.MANDATORY: "Please answer before continuing.",
    AbstractValidator.INVALID_DATE: "The date entered is not valid.  Please correct your answer."
}

q1.add_response(q1r2)
questionnaire.register(q1r2)

###
# Section Two
###

s2 = Section()
s2.id = "d9d25a21-41b8-42b2-ac7b-fb21b1036d71"
s2.title = "Commodities - Retail Turnover"
s2.description = "<p>- You should enter figures for the reporting period stated above<br>- You should round your figures to the nearest (£) pound</p><h4>Include</h4><ul><li>VAT</li><li>Internet Sales</li></ul>"  # NOQA

b1.add_section(s2)
questionnaire.register(s2)

q2 = Question()
q2.id = "eedb9f9f-2f2e-41f4-9186-ba7110d9e6a4"
q2.title = ""
q2.description = ""
q2.type = "Currency"

s2.add_question(q2)
questionnaire.register(q2)

q2r = Response()
q2r.id = "bb8168e6-2272-450d-b5a7-d3170508efb2"
q2r.code = "22"
q2r.label = "What was the value of the business's total sales of food?"
q2r.guidance = "<div> <h4>Include</h4> <ul> <li>all fresh food</li> <li>other food for human consumption (except chocolate and sugar confectionery)</li> <li>soft drinks</li> </ul> </div> <div> <h4>Exclude</h4> <ul> <li>sales from catering facilities used by customers</li> </ul> </div>"  # NOQA
q2r.type = "Currency"
q2r.options = []
q2r.mandatory = False
q2r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q2.add_response(q2r)
questionnaire.register(q2r)

q3 = Question()
q3.id = "5743fe04-e9a3-491f-b475-ea5be662eff3"
q3.title = ""
q3.description = ""
q3.type = "Currency"

s2.add_question(q3)
questionnaire.register(q3)

q3r = Response()
q3r.id = "fee0b9fe-4c3a-4c14-9611-4fa9e2e9578a"
q3r.code = "23"
q3r.label = "What was the value of the business's total sales of alcohol, confectionery and tobacco?"
q3r.guidance = "<div> <h4>Include</h4> <ul> <li>alcoholic drink</li> <li>chocolate and sugar confectionery</li> <li>tobacco and smokers’ requisites</li></ul> </div>"  # NOQA
q3r.type = "Currency"
q3r.options = []
q3r.mandatory = False
q3r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q3.add_response(q3r)
questionnaire.register(q3r)

q4 = Question()
q4.id = "475471a1-7be0-4a7a-82b3-2b803d3935ed"
q4.title = ""
q4.description = ""
q4.type = "Currency"

s2.add_question(q4)
questionnaire.register(q4)

q4r = Response()
q4r.id = "01ac2ebf-d49d-45e8-8f7a-0f847aa7cf25"
q4r.code = "24"
q4r.label = "What was the value of the business's total sales of clothing and footwear?"
q4r.guidance = "<div> <h4>Include</h4><ul> <li>clothing and footwear</li> <li>clothing fabrics</li> <li>haberdashery and furs</li> <li>leather and travel goods</li> <li>handbags</li> <li>umbrellas</li></ul></div>"  # NOQA
q4r.type = "Currency"
q4r.options = []
q4r.mandatory = False
q4r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q4.add_response(q4r)
questionnaire.register(q4r)

q5 = Question()
q5.id = "656eaad2-67ed-4413-93dd-06d66c954a22"
q5.title = ""
q5.description = ""
q5.type = "Currency"

s2.add_question(q5)
questionnaire.register(q5)

q5r = Response()
q5r.id = "7605c4a9-2c3a-483c-908b-e07244105ac4"
q5r.code = "25"
q5r.label = "What was the value of the business's total sales of household goods?"
q5r.guidance = "<div> <h4>Include</h4><ul> <li>carpets, rugs and other floor coverings</li> <li>furniture</li> <li>household textiles and soft furnishings</li> <li>prints and picture frames</li> <li>antiques and works of art</li> <li>domestic electrical and gas appliances, audio/visual equipment and home computers</li> <li>lighting and minor electrical supplies</li> <li>records, compact discs, audio and video tapes</li> <li>musical instruments and goods</li> <li>decorators’ and DIY supplies</li> <li>lawn-mowers</li> <li>hardware</li> <li>china, glassware and cutlery</li> <li>novelties, souvenirs and gifts</li> <li>e-cigarettes</li> </ul></div>"  # NOQA
q5r.type = "Currency"
q5r.options = []
q5r.mandatory = False
q5r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q5.add_response(q5r)
questionnaire.register(q5r)

q6 = Question()
q6.id = "d7144593-8899-434a-8630-c622df1689b2"
q6.title = ""
q6.description = ""
q6.type = "Currency"

s2.add_question(q6)
questionnaire.register(q6)

q6r = Response()
q6r.id = "5843e26e-a139-4645-baa9-51bdb0aba27b"
q6r.code = "26"
q6r.label = "What was the value of the business’s total sales of other goods?"
q6r.guidance = "<div> <h4>Include</h4> <ul>  <li>toiletries and medications (except NHS receipts)</li> <li>newspapers and periodicals</li> <li>books, stationery and office supplies</li> <li>photographic and optical goods</li> <li>spectacles, contact lenses and sunglasses</li> <li>toys and games</li> <li>cycles and cycle accessories</li> <li>sport and camping equipment</li> <li>jewellery</li> <li>silverware and plate, clocks and watches</li> <li>household cleaning products and kitchen paper products</li> <li>pets, pets’ requisites and pet foods</li> <li>cut flowers, plants, seeds and other garden sundries</li> <li>other new and second hand goods</li> <li>Mobile phones</li> </ul> </div> <div> <h4>Exclude</h4> <ul> <li>revenue from mobile phone network commission and top up </li> <li>lottery sales and commission from lottery sales</li> <li>sales of car accessories and motor vehicles</li> <li>NHS receipts</li> </ul> </div>"  # NOQA
q6r.type = "Currency"
q6r.options = []
q6r.mandatory = False
q6r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q6.add_response(q6r)
questionnaire.register(q6r)

q7 = Question()
q7.id = "6c302f72-cf9d-4f42-8a35-cb258c3f807c"
q7.title = ""
q7.description = ""
q7.type = "Currency"

s2.add_question(q7)
questionnaire.register(q7)

q7r = Response()
q7r.id = "e81adc6d-6fb0-4155-969c-d0d646f15345"
q7r.code = "20"
q7r.label = "What was the value of the business’s total retail turnover?"
q7r.guidance = "<div> <h4>Include</h4> <ul> <li>VAT</li> <li>internet sales</li> <li>retail sale from outlets in Great Britain to customers abroad</li> </ul> </div> <div> <h4>Exclude</h4> <ul> <li>revenue from mobile phone network commission and top up </li> <li>sales from catering facilities used by customers</li>  <li>lottery sales and commission from lottery sales</li> <li>sales of car accessories and motor vehicles</li> <li>NHS receipts</li> </ul> </div>"  # NOQA
q7r.type = "Currency"
q7r.options = []
q7r.mandatory = True
q7r.messages = {
    AbstractValidator.MANDATORY: "Please provide a value, even if your value is 0.",
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q7.add_response(q7r)
questionnaire.register(q7r)

q8 = Question()
q8.id = "c9902a3b-7dbb-48ff-8d3f-dce6fef322c7"
q8.title = ""
q8.description = ""
q8.type = "Currency"

s2.add_question(q8)
questionnaire.register(q8)

q8r = Response()
q8r.id = "4b75a6f7-9774-4b2b-82dc-976561189a99"
q8r.code = "21"
q8r.label = "Of your total retail turnover, how much were from internet sales?"
q8r.guidance = "<div> <h4>Include</h4><ul> <li>VAT</li> <li>sales from orders received over the internet, irrespective of the payment or delivery method</li> </ul></div>"  # NOQA
q8r.type = "Currency"
q8r.options = []
q8r.mandatory = False
q8r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q8.add_response(q8r)
questionnaire.register(q8r)

q9 = Question()
q9.id = "96984134-1863-4450-b314-c44cf48d2bcd"
q9.title = ""
q9.description = ""
q9.type = "Currency"

s2.add_question(q9)
questionnaire.register(q9)

q9r = Response()
q9r.id = "b2bac3ed-5504-43ef-a883-f9ca8496aca3"
q9r.code = "27"
q9r.label = "What was the value of the business’s total sales of automotive fuel?"
q9r.guidance = "<div><h4>Include</h4><ul> <li>VAT</li> <li>sales of fuel owned by you</li> <li>sales of other items not paid a commission for</li>  </ul></div><div> <h4>Exclude</h4> <ul> <li>sales of fuel not owned by you</li> <li>any commissions</li> </ul></div>"  # NOQA
q9r.type = "Currency"
q9r.options = []
q9r.mandatory = False
q9r.messages = {
    AbstractValidator.NOT_INTEGER: "Please only enter whole numbers into the field.",
    AbstractValidator.NEGATIVE_INTEGER: "The value cannot be negative. Please correct your answer.",
    AbstractValidator.INTEGER_TOO_LARGE: "The maximum value allowed is 9999999999. Please correct your answer."
}

q9.add_response(q9r)
questionnaire.register(q9r)

###
# Section Three
###

s3 = Section()
s3.id = "94546782-08a6-4213-9dc9-0780c2996896"
s3.title = "Comments"
s3.description = ""

b1.add_section(s3)
questionnaire.register(s3)

q10 = Question()
q10.id = "fef6edc2-d98c-4d4d-9a7c-997ce10c361f"
q10.title = ""
q10.description = "Please explain any movements in your data e.g. sale held, branches opened or sold, extreme weather, or temporary closure of shop"

q10.type = "Textarea"

s3.add_question(q10)
questionnaire.register(q10)

q10r = Response()
q10r.id = "215015b1-f87c-4740-9fd4-f01f707ef558"
q10r.code = "146"
q10r.label = ""
q10r.guidance = ""
q10r.type = "Textarea"
q10r.options = []
q10r.mandatory = False

q10.add_response(q10r)
questionnaire.register(q10r)

q10r_display = Display()
q10r_display.properties = {
    "max_length": "2000"
}
q10r.display = q10r_display
