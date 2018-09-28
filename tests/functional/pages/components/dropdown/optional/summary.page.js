// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownOptionalAnswer(index = 0 ) { return '#dropdown-optional-answer-' + index + '-answer'; }

  dropdownOptionalAnswerEdit(index = 0) { return '[data-qa="dropdown-optional-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
