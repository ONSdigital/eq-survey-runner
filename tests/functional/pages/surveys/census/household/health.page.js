// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class HealthPage extends QuestionPage {

  constructor() {
    super('health');
  }

  veryGood() {
    return '#health-answer-0';
  }

  veryGoodLabel() { return '#label-health-answer-0'; }

  good() {
    return '#health-answer-1';
  }

  goodLabel() { return '#label-health-answer-1'; }

  fair() {
    return '#health-answer-2';
  }

  fairLabel() { return '#label-health-answer-2'; }

  bad() {
    return '#health-answer-3';
  }

  badLabel() { return '#label-health-answer-3'; }

  veryBad() {
    return '#health-answer-4';
  }

  veryBadLabel() { return '#label-health-answer-4'; }

}
module.exports = new HealthPage();
