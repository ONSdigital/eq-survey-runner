// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class DateOfBirthPage extends QuestionPage {

  constructor() {
    super('date-of-birth');
  }

  day() {
    return '#date-of-birth-answer-day';
  }

  month() {
    return '#date-of-birth-answer-month';
  }

  year() {
    return '#date-of-birth-answer-year';
  }

}
module.exports = new DateOfBirthPage();
