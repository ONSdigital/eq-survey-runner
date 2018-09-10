// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  setMinimum(index = 0) { return '#set-minimum-' + index + '-answer'; }

  setMinimumEdit(index = 0) { return '[data-qa="set-minimum-' + index + '-edit"]'; }

  setMaximum(index = 0) { return '#set-maximum-' + index + '-answer'; }

  setMaximumEdit(index = 0) { return '[data-qa="set-maximum-' + index + '-edit"]'; }

  testRange(index = 0) { return '#test-range-' + index + '-answer'; }

  testRangeEdit(index = 0) { return '[data-qa="test-range-' + index + '-edit"]'; }

  testMin(index = 0) { return '#test-min-' + index + '-answer'; }

  testMinEdit(index = 0) { return '[data-qa="test-min-' + index + '-edit"]'; }

  testMax(index = 0) { return '#test-max-' + index + '-answer'; }

  testMaxEdit(index = 0) { return '[data-qa="test-max-' + index + '-edit"]'; }

  testPercent(index = 0) { return '#test-percent-' + index + '-answer'; }

  testPercentEdit(index = 0) { return '[data-qa="test-percent-' + index + '-edit"]'; }

  testDecimal(index = 0) { return '#test-decimal-' + index + '-answer'; }

  testDecimalEdit(index = 0) { return '[data-qa="test-decimal-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
