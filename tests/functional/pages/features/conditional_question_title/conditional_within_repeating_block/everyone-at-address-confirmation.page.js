// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class EveryoneAtAddressConfirmationPage extends QuestionPage {

  constructor() {
    super('everyone-at-address-confirmation');
  }

  yes() {
    return '#everyone-at-address-confirmation-answer-0';
  }

  yesLabel() { return '#label-everyone-at-address-confirmation-answer-0'; }

  no() {
    return '#everyone-at-address-confirmation-answer-1';
  }

  noLabel() { return '#label-everyone-at-address-confirmation-answer-1'; }

}
module.exports = new EveryoneAtAddressConfirmationPage();
