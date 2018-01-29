// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownMandatoryWithOverriddenAnswer() { return '#dropdown-mandatory-with-overridden-answer-answer'; }

  dropdownMandatoryWithOverriddenAnswerEdit() { return '[data-qa="dropdown-mandatory-with-overridden-answer-edit"]'; }

}
module.exports = new SummaryPage();
