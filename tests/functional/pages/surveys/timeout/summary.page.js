// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  timeoutAnswer(index = 0) { return '#timeout-answer-' + index + '-answer'; }

  timeoutAnswerEdit(index = 0) { return '[data-qa="timeout-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
