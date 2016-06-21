import copy

from app.surveys.mci_0205 import mci_0205

form_type = "0203"

# The 0203 Form is the same as 0205 but without the fuel question
# Copy the survey first by exporting and then reimporting
mci_0203 = copy.deepcopy(mci_0205)
mci_0203.eq_id = "1"

# Remove the question from the questionnaire
question = mci_0203.get_item_by_id("96984134-1863-4450-b314-c44cf48d2bcd")
section = question.container
section.questions.remove(question)

# Unregister the question
mci_0203.unregister("96984134-1863-4450-b314-c44cf48d2bcd")
# Unregister the response
mci_0203.unregister("4b75a6f7-9774-4b2b-82dc-976561189a99")
