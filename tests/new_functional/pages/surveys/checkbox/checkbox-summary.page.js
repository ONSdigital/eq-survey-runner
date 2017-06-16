const QuestionPage = require('../question.page');

class CheckboxSummaryPage extends QuestionPage {

  mandatoryAnswer() {
    return '#mandatory-checkbox-answer-answer';
  }

  nonMandatoryAnswer() {
    return '#non-mandatory-checkbox-answer-answer';
  }

  mandatoryOtherAnswer() {
    return '[data-qa="other-answer-mandatory-answer"]';
  }

  nonMandatoryOtherAnswer() {
    return '#other-answer-non-mandatory-answer';
  }

}

module.exports = new CheckboxSummaryPage();
