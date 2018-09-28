// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  dateRangeFromAnswer(index = 0) {
    return '#date-range-from-' + index + '-answer';
  }

  monthYearAnswer(index = 0) {
    return '#month-year-answer-' + index + '-answer';
  }

  singleDateAnswer(index = 0) {
    return '#single-date-answer-' + index + '-answer';
  }

  nonMandatoryDateAnswer(index = 0) {
    return '#non-mandatory-date-answer-' + index + '-answer';
  }

}
module.exports = new SummaryPage();
