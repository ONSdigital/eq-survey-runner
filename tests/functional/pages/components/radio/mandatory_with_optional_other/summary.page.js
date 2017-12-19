// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioMandatoryAnswer() { return '#radio-mandatory-answer-answer'; }

  radioMandatoryAnswerEdit() { return '[data-qa="radio-mandatory-answer-edit"]'; }

  otherAnswerMandatory() { return '#other-answer-mandatory-answer'; }

  otherAnswerMandatoryEdit() { return '[data-qa="other-answer-mandatory-edit"]'; }

}
module.exports = new SummaryPage();
