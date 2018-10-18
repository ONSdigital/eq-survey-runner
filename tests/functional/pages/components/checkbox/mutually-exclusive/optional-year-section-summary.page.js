// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalYearSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-year-section-summary');
  }

  yearDateAnswer(index = 0) { return '#year-date-answer-' + index + '-answer'; }

  yearDateAnswerEdit(index = 0) { return '[data-qa="year-date-answer-' + index + '-edit"]'; }

  yearDateExclusiveAnswer(index = 0) { return '#year-date-exclusive-answer-' + index + '-answer'; }

  yearDateExclusiveAnswerEdit(index = 0) { return '[data-qa="year-date-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveYearDateQuestion(index = 0) { return '#mutually-exclusive-year-date-question-' + index; }

  mutuallyExclusiveYearDateGroupTitle(index = 0) { return '#mutually-exclusive-year-date-group-' + index; }

  mutuallyExclusiveYearSectionSummaryTitle(index = 0) { return '#mutually-exclusive-year-section-summary-' + index; }

}
module.exports = new OptionalYearSectionSummaryPage();
