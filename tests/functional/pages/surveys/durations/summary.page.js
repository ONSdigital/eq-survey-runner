// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  yearMonthAnswer() { return '#year-month-answer-answer'; }

  yearMonthAnswerEdit() { return '[data-qa="year-month-answer-edit"]'; }

  mandatoryYearMonthAnswer() { return '#mandatory-year-month-answer-answer'; }

  mandatoryYearMonthAnswerEdit() { return '[data-qa="mandatory-year-month-answer-edit"]'; }

  yearAnswer() { return '#year-answer-answer'; }

  yearAnswerEdit() { return '[data-qa="year-answer-edit"]'; }

  mandatoryYearAnswer() { return '#mandatory-year-answer-answer'; }

  mandatoryYearAnswerEdit() { return '[data-qa="mandatory-year-answer-edit"]'; }

  monthAnswer() { return '#month-answer-answer'; }

  monthAnswerEdit() { return '[data-qa="month-answer-edit"]'; }

  mandatoryMonthAnswer() { return '#mandatory-month-answer-answer'; }

  mandatoryMonthAnswerEdit() { return '[data-qa="mandatory-month-answer-edit"]'; }

  durationsTitle() { return '#durations'; }

}
module.exports = new SummaryPage();
