// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalMonthYearSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-month-year-section-summary');
  }

  monthYearDateAnswer(index = 0) { return '#month-year-date-answer-' + index + '-answer'; }

  monthYearDateAnswerEdit(index = 0) { return '[data-qa="month-year-date-answer-' + index + '-edit"]'; }

  monthYearDateExclusiveAnswer(index = 0) { return '#month-year-date-exclusive-answer-' + index + '-answer'; }

  monthYearDateExclusiveAnswerEdit(index = 0) { return '[data-qa="month-year-date-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveMonthYearDateQuestion(index = 0) { return '#mutually-exclusive-month-year-date-question-' + index; }

  mutuallyExclusiveMonthYearDateGroupTitle(index = 0) { return '#mutually-exclusive-month-year-date-group-' + index; }

  mutuallyExclusiveMonthYearSectionSummaryTitle(index = 0) { return '#mutually-exclusive-month-year-section-summary-' + index; }

}
module.exports = new OptionalMonthYearSectionSummaryPage();
