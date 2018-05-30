// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  answer() { return '#mandatory-checkbox-answer-answer'; }

  answerEdit() { return '[data-qa="mandatory-checkbox-answer-edit"]'; }

  checkboxesTitle() { return '#checkboxes'; }

}
module.exports = new SummaryPage();
