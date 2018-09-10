// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  answer(index = 0) { return '#mandatory-checkbox-answer-' + index + '-answer'; }

  answerEdit(index = 0) { return '[data-qa="mandatory-checkbox-answer-' + index + '-edit"]'; }

  checkboxesTitle(index = 0) { return '#checkboxes' + index; }

}
module.exports = new SummaryPage();
