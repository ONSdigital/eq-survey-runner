// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveNumberPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-number');
  }

  number() {
    return '#number-answer';
  }

  numberLabel() { return '#label-number-answer'; }

  numberExclusiveIPreferNotToSay() {
    return '#number-exclusive-answer-0';
  }

  numberExclusiveIPreferNotToSayLabel() { return '#label-number-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveNumberPage();
