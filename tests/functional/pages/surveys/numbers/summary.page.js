// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  setMinimum() { return '#set-minimum-answer'; }

  setMinimumEdit() { return '[data-qa="set-minimum-edit"]'; }

  setMaximum() { return '#set-maximum-answer'; }

  setMaximumEdit() { return '[data-qa="set-maximum-edit"]'; }

  testRange() { return '#test-range-answer'; }

  testRangeEdit() { return '[data-qa="test-range-edit"]'; }

  testMin() { return '#test-min-answer'; }

  testMinEdit() { return '[data-qa="test-min-edit"]'; }

  testMax() { return '#test-max-answer'; }

  testMaxEdit() { return '[data-qa="test-max-edit"]'; }

  testPercent() { return '#test-percent-answer'; }

  testPercentEdit() { return '[data-qa="test-percent-edit"]'; }

  testDecimal() { return '#test-decimal-answer'; }

  testDecimalEdit() { return '[data-qa="test-decimal-edit"]'; }

}
module.exports = new SummaryPage();
