const QuestionPage = require('../question.page');

class CheckboxSummaryPage extends QuestionPage {

  mandatoryAnswer(index = 0) {
    return '#mandatory-checkbox-answer-' + index + '-answer';
  }

  nonMandatoryAnswer(index = 0) {
    return '#non-mandatory-checkbox-answer-' + index + '-answer';
  }

  mandatoryOtherAnswer(index = 0) {
    return '[data-qa="other-answer-mandatory-' + index + '-answer"]';
  }

  nonMandatoryOtherAnswer(index = 0) {
    return '#other-answer-non-mandatory-' + index + '-answer';
  }

}

module.exports = new CheckboxSummaryPage();
