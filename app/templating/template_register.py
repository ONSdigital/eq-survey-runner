from app.templating.questionnaire_template_preprocessor import QuestionnaireTemplatePreprocessor
from app.templating.summary_template_preprocessor import SummaryTemplatePreprocessor

KNOWN_TEMPLATES = {
    'introduction': {'template': "landing-page.html", "preprocessor": QuestionnaireTemplatePreprocessor},
    'summary': {'template': "summary.html", "preprocessor": SummaryTemplatePreprocessor},
    'confirmation': {'template': "confirmation.html", "preprocessor": QuestionnaireTemplatePreprocessor},
    'thank-you': {'template': "thank-you.html", "preprocessor": QuestionnaireTemplatePreprocessor},
    'questionnaire': {'template': "questionnaire.html", "preprocessor": QuestionnaireTemplatePreprocessor},
}


class TemplateRegistry(object):

    @staticmethod
    def get_template_name(current_location):
        if current_location in KNOWN_TEMPLATES:
            return KNOWN_TEMPLATES[current_location]['template']
        else:
            # must be a valid location to get this far, so must be within the
            # questionnaire
            return KNOWN_TEMPLATES['questionnaire']['template']

    @staticmethod
    def get_template_preprocessor(current_location):
        if current_location in KNOWN_TEMPLATES:
            cls = KNOWN_TEMPLATES[current_location]['preprocessor']
        else:
            cls = KNOWN_TEMPLATES['questionnaire']['preprocessor']
        return cls()
