// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveUnitPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-unit');
  }

  unit() {
    return '#unit-answer';
  }

  unitLabel() { return '#label-unit-answer'; }

  unitUnit() {
    return '#unit-answer-type';
  }

  unitExclusiveIPreferNotToSay() {
    return '#unit-exclusive-answer-0';
  }

  unitExclusiveIPreferNotToSayLabel() { return '#label-unit-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveUnitPage();
