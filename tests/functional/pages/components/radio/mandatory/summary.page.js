// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioMandatoryAnswer(index = 0) { return '#radio-mandatory-answer-' + index + '-answer'; }

  radioMandatoryAnswerEdit(index = 0) { return '[data-qa="radio-mandatory-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
