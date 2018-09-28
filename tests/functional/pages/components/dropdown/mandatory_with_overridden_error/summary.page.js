// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownMandatoryWithOverriddenAnswer(index = 0) { return '#dropdown-mandatory-with-overridden-answer-' + index + '-answer'; }

  dropdownMandatoryWithOverriddenAnswerEdit(index = 0) { return '[data-qa="dropdown-mandatory-with-overridden-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
