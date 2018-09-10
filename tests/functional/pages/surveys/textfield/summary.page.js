// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  answer(index = 0) { return '#answer-' + index + '-answer'; }

  answerEdit(index = 0) { return '[data-qa="answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
