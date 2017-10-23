// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class DisabilityPage extends QuestionPage {

  constructor() {
    super('disability');
  }

  yesLimitedALot() {
    return '#disability-answer-0';
  }

  yesLimitedALittle() {
    return '#disability-answer-1';
  }

  no() {
    return '#disability-answer-2';
  }

}
module.exports = new DisabilityPage();
