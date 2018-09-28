// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownMandatoryAnswer(index = 0) { return '#dropdown-mandatory-answer-' + index + '-answer'; }

  dropdownMandatoryAnswerEdit(index = 0) { return '[data-qa="dropdown-mandatory-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
