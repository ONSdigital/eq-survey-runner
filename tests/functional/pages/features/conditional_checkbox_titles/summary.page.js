// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  nameAnswer() { return '#name-answer-answer'; }

  nameAnswerEdit() { return '[data-qa="name-answer-edit"]'; }

  checkboxAnswer() { return '#checkbox-answer-answer'; }

  checkboxAnswerEdit() { return '[data-qa="checkbox-answer-edit"]'; }

  radioAnswer() { return '#radio-answer-answer'; }

  radioAnswerEdit() { return '[data-qa="radio-answer-edit"]'; }

  radioCheckboxDescriptioTitle() { return '#radio-checkbox-descriptio'; }

}
module.exports = new SummaryPage();
