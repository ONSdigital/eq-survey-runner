// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class TermTimeLocationPage extends QuestionPage {

  constructor() {
    super('term-time-location');
  }

  atYourAddress() {
    return '#term-time-location-answer-0';
  }

  atYourAddressLabel() { return '#label-term-time-location-answer-0'; }

  atAnotherAddress() {
    return '#term-time-location-answer-1';
  }

  atAnotherAddressLabel() { return '#label-term-time-location-answer-1'; }

}
module.exports = new TermTimeLocationPage();
