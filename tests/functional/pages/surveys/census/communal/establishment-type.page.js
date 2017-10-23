// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class EstablishmentTypePage extends QuestionPage {

  constructor() {
    super('establishment-type');
  }

  hotel() {
    return '#establishment-type-answer-0';
  }

  hotelLabel() { return '#label-establishment-type-answer-0'; }

  guestHouse() {
    return '#establishment-type-answer-1';
  }

  guestHouseLabel() { return '#label-establishment-type-answer-1'; }

  bB() {
    return '#establishment-type-answer-2';
  }

  bBLabel() { return '#label-establishment-type-answer-2'; }

  innPub() {
    return '#establishment-type-answer-3';
  }

  innPubLabel() { return '#label-establishment-type-answer-3'; }

  other() {
    return '#establishment-type-answer-4';
  }

  otherLabel() { return '#label-establishment-type-answer-4'; }

  otherText() {
    return '#establishment-type-answer-other';
  }

}
module.exports = new EstablishmentTypePage();
