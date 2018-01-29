// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownMandatoryWithLabelAnswer() { return '#dropdown-mandatory-with-label-answer-answer'; }

  dropdownMandatoryWithLabelAnswerEdit() { return '[data-qa="dropdown-mandatory-with-label-answer-edit"]'; }

}
module.exports = new SummaryPage();
