// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SkipPaymentPage extends QuestionPage {

  constructor() {
    super('skip-payment');
  }

  yes() {
    return '#skip-payment-answer-0';
  }

  yesLabel() { return '#label-skip-payment-answer-0'; }

  no() {
    return '#skip-payment-answer-1';
  }

  noLabel() { return '#label-skip-payment-answer-1'; }

}
module.exports = new SkipPaymentPage();
