// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class AddressTypePage extends QuestionPage {

  constructor() {
    super('address-type');
  }

  armedForcesBaseAddress() {
    return '#address-type-answer-0';
  }

  anotherAddressWhenWorkingAwayFromHome() {
    return '#address-type-answer-1';
  }

  studentSHomeAddress() {
    return '#address-type-answer-2';
  }

  studentSTermTimeAddress() {
    return '#address-type-answer-3';
  }

  anotherParentOrGuardianSAddress() {
    return '#address-type-answer-4';
  }

  holidayHome() {
    return '#address-type-answer-5';
  }

  other() {
    return '#address-type-answer-6';
  }

  otherText() {
    return '#address-type-answer-other';
  }

}
module.exports = new AddressTypePage();
