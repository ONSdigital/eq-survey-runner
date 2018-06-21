// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class DefinitionSummaryPage extends QuestionPage {

  constructor() {
    super('definition-summary');
  }

  radioMandatoryAnswer() { return '#radio-mandatory-answer-answer'; }

  radioMandatoryAnswerEdit() { return '[data-qa="radio-mandatory-answer-edit"]'; }

  definitionGroupTitle() { return '#definition-group'; }

}
module.exports = new DefinitionSummaryPage();
