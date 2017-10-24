// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class VisitorDateOfBirthPage extends QuestionPage {

  constructor() {
    super('visitor-date-of-birth');
  }

  day() {
    return '#visitor-date-of-birth-answer-day';
  }

  month() {
    return '#visitor-date-of-birth-answer-month';
  }

  year() {
    return '#visitor-date-of-birth-answer-year';
  }

}
module.exports = new VisitorDateOfBirthPage();
