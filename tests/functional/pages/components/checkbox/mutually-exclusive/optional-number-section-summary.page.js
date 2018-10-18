// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalNumberSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-number-section-summary');
  }

  numberAnswer(index = 0) { return '#number-answer-' + index + '-answer'; }

  numberAnswerEdit(index = 0) { return '[data-qa="number-answer-' + index + '-edit"]'; }

  numberExclusiveAnswer(index = 0) { return '#number-exclusive-answer-' + index + '-answer'; }

  numberExclusiveAnswerEdit(index = 0) { return '[data-qa="number-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveNumberQuestion(index = 0) { return '#mutually-exclusive-number-question-' + index; }

  mutuallyExclusiveNumberGroupTitle(index = 0) { return '#mutually-exclusive-number-group-' + index; }

  mutuallyExclusiveNumberSectionSummaryTitle(index = 0) { return '#mutually-exclusive-number-section-summary-' + index; }

}
module.exports = new OptionalNumberSectionSummaryPage();
