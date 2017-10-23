// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class AnotherAddressPage extends QuestionPage {

  constructor() {
    super('another-address');
  }

  no() {
    return '#another-address-answer-0';
  }

  yesAnAddressWithinTheUk() {
    return '#another-address-answer-1';
  }

  other() {
    return '#another-address-answer-2';
  }

  otherText() {
    return '#another-address-answer-other';
  }

}
module.exports = new AnotherAddressPage();
