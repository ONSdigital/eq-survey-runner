// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class DateQuestionPage extends QuestionPage {

  constructor() {
    super('date-question');
  }

  day() {
    return '#single-date-answer-day';
  }

  month() {
    return '#single-date-answer-month';
  }

  year() {
    return '#single-date-answer-year';
  }

}
module.exports = new DateQuestionPage();
