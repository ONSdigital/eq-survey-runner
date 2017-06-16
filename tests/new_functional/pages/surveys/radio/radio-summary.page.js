const QuestionPage = require('../question.page');

class RadioSummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  otherAnswer() {
    return '#other-answer-mandatory-answer';
  }

  answer() {
    return '#radio-mandatory-answer-answer';
  }

}

module.exports = new RadioSummaryPage();
