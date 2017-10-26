const QuestionPage = require('../question.page');

class RadioSummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  otherAnswer() {
    return '#other-answer-mandatory-answer';
  }

  answer_mandatory() {
    return '#radio-mandatory-answer-answer';
  }

  answer_optional() {
    return '#radio-non-mandatory-answer-answer';
  }
}

module.exports = new RadioSummaryPage();
