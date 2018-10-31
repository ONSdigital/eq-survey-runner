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

  testRangeLabelDescription() { return '#label-test-range > .label__description'; }

  testRangeExclusive() {
    return '#test-range-exclusive';
  }

  testRangeExclusiveLabel() { return '#label-test-range-exclusive'; }

  testRangeExclusiveLabelDescription() { return '#label-test-range-exclusive > .label__description'; }

  testMin() {
    return '#test-min';
  }

  testMinLabel() { return '#label-test-min'; }

  testMinLabelDescription() { return '#label-test-min > .label__description'; }

  testMax() {
    return '#test-max';
  }

  testMaxLabel() { return '#label-test-max'; }

  testMaxLabelDescription() { return '#label-test-max > .label__description'; }

  testMinExclusive() {
    return '#test-min-exclusive';
  }

  testMinExclusiveLabel() { return '#label-test-min-exclusive'; }

  testMinExclusiveLabelDescription() { return '#label-test-min-exclusive > .label__description'; }

  testMaxExclusive() {
    return '#test-max-exclusive';
  }

  testMaxExclusiveLabel() { return '#label-test-max-exclusive'; }

  testMaxExclusiveLabelDescription() { return '#label-test-max-exclusive > .label__description'; }

  testPercent() {
    return '#test-percent';
  }

  testPercentLabel() { return '#label-test-percent'; }

  testPercentLabelDescription() { return '#label-test-percent > .label__description'; }

  testDecimal() {
    return '#test-decimal';
  }

  testDecimalLabel() { return '#label-test-decimal'; }

  testDecimalLabelDescription() { return '#label-test-decimal > .label__description'; }

}
module.exports = new TestMinMaxBlockPage();
