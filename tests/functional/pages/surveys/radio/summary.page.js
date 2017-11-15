// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioMandatoryAnswer() { return '#radio-mandatory-answer-answer'; }

  radioMandatoryAnswerEdit() { return '[data-qa="radio-mandatory-answer-edit"]'; }

  otherAnswerMandatory() { return '#other-answer-mandatory-answer'; }

  otherAnswerMandatoryEdit() { return '[data-qa="other-answer-mandatory-edit"]'; }

  radioNonMandatoryAnswer() { return '#radio-non-mandatory-answer-answer'; }

  radioNonMandatoryAnswerEdit() { return '[data-qa="radio-non-mandatory-answer-edit"]'; }

  otherAnswerNonMandatory() { return '#other-answer-non-mandatory-answer'; }

  otherAnswerNonMandatoryEdit() { return '[data-qa="other-answer-non-mandatory-edit"]'; }

}
module.exports = new SummaryPage();
