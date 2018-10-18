// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveMonthYearDatePage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-month-year-date');
  }

  monthYearDateMonth() {
    return '#month-year-date-answer-month';
  }

  monthYearDateYear() {
    return '#month-year-date-answer-year';
  }

  monthYearDateExclusiveIPreferNotToSay() {
    return '#month-year-date-exclusive-answer-0';
  }

  monthYearDateExclusiveIPreferNotToSayLabel() { return '#label-month-year-date-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveMonthYearDatePage();
