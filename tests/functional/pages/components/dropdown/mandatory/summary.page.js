// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dropdownMandatoryAnswer() { return '#dropdown-mandatory-answer-answer'; }

  dropdownMandatoryAnswerEdit() { return '[data-qa="dropdown-mandatory-answer-edit"]'; }

}
module.exports = new SummaryPage();
