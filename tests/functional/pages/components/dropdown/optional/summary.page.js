// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownOptionalAnswer() { return '#dropdown-optional-answer-answer'; }

  dropdownOptionalAnswerEdit() { return '[data-qa="dropdown-optional-answer-edit"]'; }

}
module.exports = new SummaryPage();
