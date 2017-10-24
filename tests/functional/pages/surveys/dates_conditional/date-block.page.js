// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class DateBlockPage extends QuestionPage {

  constructor() {
    super('date-block');
  }

  dateStartFromday() {
    return '#date-start-from-day';
  }

  dateStartFrommonth() {
    return '#date-start-from-month';
  }

  dateStartFromyear() {
    return '#date-start-from-year';
  }

  dateEndToday() {
    return '#date-end-to-day';
  }

  dateEndTomonth() {
    return '#date-end-to-month';
  }

  dateEndToyear() {
    return '#date-end-to-year';
  }

}
module.exports = new DateBlockPage();
