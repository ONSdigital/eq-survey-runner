// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ApproachedTelephonePage extends QuestionPage {

  constructor() {
    super('approached-telephone');
  }

  yes() {
    return '#approached-telephone-answer-0';
  }

  yesLabel() { return '#label-approached-telephone-answer-0'; }

  no() {
    return '#approached-telephone-answer-1';
  }

  noLabel() { return '#label-approached-telephone-answer-1'; }

}
module.exports = new ApproachedTelephonePage();
