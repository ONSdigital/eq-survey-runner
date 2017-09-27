// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dateRangeFromAnswer() {
    return '#date-range-from-answer';
  }

  monthYearAnswer() {
    return '#month-year-answer-answer';
  }

  singleDateAnswer() {
    return '#single-date-answer-answer';
  }

  nonMandatoryDateAnswer() {
    return '#non-mandatory-date-answer-answer';
  }

}
module.exports = new SummaryPage();
