// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  yearMonthAnswer(index = 0) { return '#year-month-answer-' + index + '-answer'; }

  yearMonthAnswerEdit(index = 0) { return '[data-qa="year-month-answer-' + index + '-edit"]'; }

  mandatoryYearMonthAnswer(index = 0) { return '#mandatory-year-month-answer-' + index + '-answer'; }

  mandatoryYearMonthAnswerEdit(index = 0) { return '[data-qa="mandatory-year-month-answer-' + index + '-edit"]'; }

  yearAnswer(index = 0) { return '#year-answer-' + index + '-answer'; }

  yearAnswerEdit(index = 0) { return '[data-qa="year-answer-' + index + '-edit"]'; }

  mandatoryYearAnswer(index = 0) { return '#mandatory-year-answer-' + index + '-answer'; }

  mandatoryYearAnswerEdit(index = 0) { return '[data-qa="mandatory-year-answer-' + index + '-edit"]'; }

  monthAnswer(index = 0) { return '#month-answer-' + index + '-answer'; }

  monthAnswerEdit(index = 0) { return '[data-qa="month-answer-' + index + '-edit"]'; }

  mandatoryMonthAnswer(index = 0) { return '#mandatory-month-answer-' + index + '-answer'; }

  mandatoryMonthAnswerEdit(index = 0) { return '[data-qa="mandatory-month-answer-' + index + '-edit"]'; }

  durationsTitle(index = 0) { return '#durations-' + index; }

}
module.exports = new SummaryPage();
