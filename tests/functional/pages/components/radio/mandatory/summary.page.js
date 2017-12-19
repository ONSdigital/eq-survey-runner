// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioMandatoryAnswer() { return '#radio-mandatory-answer-answer'; }

  radioMandatoryAnswerEdit() { return '[data-qa="radio-mandatory-answer-edit"]'; }

}
module.exports = new SummaryPage();
