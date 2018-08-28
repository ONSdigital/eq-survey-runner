// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class DateSeparateBlockPage extends QuestionPage {

  constructor() {
    super('date-separate-block');
  }

  yes() {
    return '#date-separate-radio-0';
  }

  yesLabel() { return '#label-date-separate-radio-0'; }

  no() {
    return '#date-separate-radio-1';
  }

  noLabel() { return '#label-date-separate-radio-1'; }

}
module.exports = new DateSeparateBlockPage();
