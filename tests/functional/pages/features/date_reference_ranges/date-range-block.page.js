// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class DateRangeBlockPage extends QuestionPage {

  constructor() {
    super('date-range-block');
  }

  yes() {
    return '#date-range-radio-0';
  }

  yesLabel() { return '#label-date-range-radio-0'; }

  no() {
    return '#date-range-radio-1';
  }

  noLabel() { return '#label-date-range-radio-1'; }

}
module.exports = new DateRangeBlockPage();
