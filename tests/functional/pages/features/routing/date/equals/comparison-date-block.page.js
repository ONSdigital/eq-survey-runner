// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class ComparisonDateBlockPage extends QuestionPage {

  constructor() {
    super('comparison-date-block');
  }

  day() {
    return '#comparison-date-answer-day';
  }

  month() {
    return '#comparison-date-answer-month';
  }

  year() {
    return '#comparison-date-answer-year';
  }

}
module.exports = new ComparisonDateBlockPage();
