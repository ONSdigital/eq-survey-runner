// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class DateBlockPage extends QuestionPage {

  constructor() {
    super('date-block');
  }

  day() {
    return '#date-day';
  }

  month() {
    return '#date-month';
  }

  year() {
    return '#date-year';
  }

}
module.exports = new DateBlockPage();
