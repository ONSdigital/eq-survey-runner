// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  timeoutAnswer() { return '#timeout-answer-answer'; }

  timeoutAnswerEdit() { return '[data-qa="timeout-answer-edit"]'; }

}
module.exports = new SummaryPage();
