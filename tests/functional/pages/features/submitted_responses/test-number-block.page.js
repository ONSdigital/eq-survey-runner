// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class TestNumberBlockPage extends QuestionPage {

  constructor() {
    super('test-number-block');
  }

  testCurrency() {
    return '#test-currency';
  }

  testCurrencyLabel() { return '#label-test-currency'; }

  squareKilometres() {
    return '#square-kilometres';
  }

  squareKilometresLabel() { return '#label-square-kilometres'; }

  testDecimal() {
    return '#test-decimal';
  }

  testDecimalLabel() { return '#label-test-decimal'; }

}
module.exports = new TestNumberBlockPage();
