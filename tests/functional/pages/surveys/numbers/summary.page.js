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

  setMinQuestion(index = 0) { return '#set-min-question-' + index; }

  testRange(index = 0) { return '#test-range-' + index + '-answer'; }

  testRangeEdit(index = 0) { return '[data-qa="test-range-' + index + '-edit"]'; }

  testRangeExclusive(index = 0) { return '#test-range-exclusive-' + index + '-answer'; }

  testRangeExclusiveEdit(index = 0) { return '[data-qa="test-range-exclusive-' + index + '-edit"]'; }

  testMin(index = 0) { return '#test-min-' + index + '-answer'; }

  testMinEdit(index = 0) { return '[data-qa="test-min-' + index + '-edit"]'; }

  testMax(index = 0) { return '#test-max-' + index + '-answer'; }

  testMaxEdit(index = 0) { return '[data-qa="test-max-' + index + '-edit"]'; }

  testMinExclusive(index = 0) { return '#test-min-exclusive-' + index + '-answer'; }

  testMinExclusiveEdit(index = 0) { return '[data-qa="test-min-exclusive-' + index + '-edit"]'; }

  testMaxExclusive(index = 0) { return '#test-max-exclusive-' + index + '-answer'; }

  testMaxExclusiveEdit(index = 0) { return '[data-qa="test-max-exclusive-' + index + '-edit"]'; }

  testPercent(index = 0) { return '#test-percent-' + index + '-answer'; }

  testPercentEdit(index = 0) { return '[data-qa="test-percent-' + index + '-edit"]'; }

  testDecimal(index = 0) { return '#test-decimal-' + index + '-answer'; }

  testDecimalEdit(index = 0) { return '[data-qa="test-decimal-' + index + '-edit"]'; }

  testMinMaxRangeQuestion(index = 0) { return '#test-min-max-range-question-' + index; }

  testTitle(index = 0) { return '#test-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
