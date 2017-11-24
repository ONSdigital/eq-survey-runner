// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class TestMinMaxBlockPage extends QuestionPage {

  constructor() {
    super('test-min-max-block');
  }

  testRange() {
    return '#test-range';
  }

  testRangeLabel() { return '#label-test-range'; }

  testRangeExclusive() {
    return '#test-range-exclusive';
  }

  testRangeLabelExclusive() { return '#label-test-range-exclusive'; }


  testMin() {
    return '#test-min';
  }

  testMinLabel() { return '#label-test-min'; }

  testMax() {
    return '#test-max';
  }

  testMaxLabel() { return '#label-test-max'; }

  testMinExclusive() {
    return '#test-min-exclusive';
  }

  testMinLabelExclusive() { return '#label-test-min-exclusive'; }

  testMaxExclusive() {
    return '#test-max-exclusive';
  }

  testMaxLabelExclusive() { return '#label-test-max-exclusive'; }


  testPercent() {
    return '#test-percent';
  }

  testPercentLabel() { return '#label-test-percent'; }

  testDecimal() {
    return '#test-decimal';
  }

  testDecimalLabel() { return '#label-test-decimal'; }

}
module.exports = new TestMinMaxBlockPage();
