// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class PastUsualAddressPage extends QuestionPage {

  constructor() {
    super('past-usual-address');
  }

  thisAddress() {
    return '#past-usual-address-answer-0';
  }

  thisAddressLabel() { return '#label-past-usual-address-answer-0'; }

  studentTermTimeOrBoardingSchoolAddressInTheUk() {
    return '#past-usual-address-answer-1';
  }

  studentTermTimeOrBoardingSchoolAddressInTheUkLabel() { return '#label-past-usual-address-answer-1'; }

  anotherAddressInTheUk() {
    return '#past-usual-address-answer-2';
  }

  anotherAddressInTheUkLabel() { return '#label-past-usual-address-answer-2'; }

  other() {
    return '#past-usual-address-answer-3';
  }

  otherLabel() { return '#label-past-usual-address-answer-3'; }

  otherText() {
    return '#past-usual-address-answer-other';
  }

}
module.exports = new PastUsualAddressPage();
