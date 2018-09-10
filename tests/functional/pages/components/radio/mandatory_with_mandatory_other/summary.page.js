// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioMandatoryAnswer(index = 0) { return '#radio-mandatory-answer-' + index + '-answer'; }

  radioMandatoryAnswerEdit(index = 0) { return '[data-qa="radio-mandatory-answer-' + index + '-edit"]'; }

  otherAnswerMandatory(index = 0) { return '#other-answer-mandatory-' + index + '-answer'; }

  otherAnswerMandatoryEdit(index = 0) { return '[data-qa="other-answer-mandatory-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
