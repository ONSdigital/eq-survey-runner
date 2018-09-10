// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioNonMandatoryAnswer(index = 0) { return '#radio-non-mandatory-answer-' + index + '-answer'; }

  radioNonMandatoryAnswerEdit(index = 0) { return '[data-qa="radio-non-mandatory-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
