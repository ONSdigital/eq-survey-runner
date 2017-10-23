// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class TestErrorsPage extends QuestionPage {

  constructor() {
    super('test-errors');
  }

  testNumber() {
    return '#test-number';
  }

  testNumberLabel() { return '#label-test-number'; }

  testPercent() {
    return '#test-percent';
  }

  testPercentLabel() { return '#label-test-percent'; }

  testCurrency() {
    return '#test-currency';
  }

  testCurrencyLabel() { return '#label-test-currency'; }

  checkError(answer) {
    return '#container-test-' + answer + '> aside > div.panel__header > ul > li';
  }

}
module.exports = new TestErrorsPage();
