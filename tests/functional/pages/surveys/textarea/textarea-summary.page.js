// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class TextareaSummaryPage extends QuestionPage {

  constructor() {
    super('textarea-summary');
  }

  answer(index = 0) {
    return '#answer-' + index + '-answer ';
  }

  answerEdit(index = 0) { return '[data-qa="answer-' + index + '-edit"]'; }

}
module.exports = new TextareaSummaryPage();
