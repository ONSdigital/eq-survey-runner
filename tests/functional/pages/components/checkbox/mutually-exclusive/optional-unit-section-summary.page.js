// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalUnitSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-unit-section-summary');
  }

  unitAnswer(index = 0) { return '#unit-answer-' + index + '-answer'; }

  unitAnswerEdit(index = 0) { return '[data-qa="unit-answer-' + index + '-edit"]'; }

  unitExclusiveAnswer(index = 0) { return '#unit-exclusive-answer-' + index + '-answer'; }

  unitExclusiveAnswerEdit(index = 0) { return '[data-qa="unit-exclusive-answer-' + index + '-edit"]'; }

}
module.exports = new OptionalUnitSectionSummaryPage();
