// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  answer(index = 0) {
    return '#date-start-from-' + index + '-answer';
  }

  otheranswer(index = 0) {
    return '#date-test-answer-' + index + '-answer';
  }

}
module.exports = new SummaryPage();
