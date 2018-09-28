// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownMandatoryWithLabelAnswer(index = 0) { return '#dropdown-mandatory-with-label-answer-' + index + '-answer'; }

  dropdownMandatoryWithLabelAnswerEdit(index = 0) { return '[data-qa="dropdown-mandatory-with-label-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
