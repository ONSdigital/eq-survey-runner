// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  answer(index = 0) { return '#answer-' + index + '-answer'; }

  answerEdit(index = 0) { return '[data-qa="answer-' + index + '-edit"]'; }

  groupTitle(index = 0) { return '#group-' + index; }

}
module.exports = new SummaryPage();
