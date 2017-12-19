// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioNonMandatoryAnswer() { return '#radio-non-mandatory-answer-answer'; }

  radioNonMandatoryAnswerEdit() { return '[data-qa="radio-non-mandatory-answer-edit"]'; }

}
module.exports = new SummaryPage();
