// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class AddressDurationPage extends QuestionPage {

  constructor() {
    super('address-duration');
  }

  yes() {
    return '#address-duration-answer-0';
  }

  yesLabel() { return '#label-address-duration-answer-0'; }

  no() {
    return '#address-duration-answer-1';
  }

  noLabel() { return '#label-address-duration-answer-1'; }

}
module.exports = new AddressDurationPage();
