// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  nameAnswer(index = 0) { return '#name-answer-' + index + '-answer'; }

  nameAnswerEdit(index = 0) { return '[data-qa="name-answer-' + index + '-edit"]'; }

  checkboxAnswer(index = 0) { return '#checkbox-answer-' + index + '-answer'; }

  checkboxAnswerEdit(index = 0) { return '[data-qa="checkbox-answer-' + index + '-edit"]'; }

  radioAnswer(index = 0) { return '#radio-answer-' + index + '-answer'; }

  radioAnswerEdit(index = 0) { return '[data-qa="radio-answer-' + index + '-edit"]'; }

  radioCheckboxDescriptioTitle(index = 0) { return '#radio-checkbox-descriptio-' + index; }

}
module.exports = new SummaryPage();
