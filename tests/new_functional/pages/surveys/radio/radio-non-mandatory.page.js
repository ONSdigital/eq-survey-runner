// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RadioNonMandatoryPage extends QuestionPage {

  constructor() {
    super('radio-non-mandatory');
  }

  none() {
    return '#radio-non-mandatory-answer-0';
  }

  noneLabel() { return '#label-radio-non-mandatory-answer-0'; }

  toast() {
    return '#radio-non-mandatory-answer-1';
  }

  toastLabel() { return '#label-radio-non-mandatory-answer-1'; }

  coffee() {
    return '#radio-non-mandatory-answer-2';
  }

  coffeeLabel() { return '#label-radio-non-mandatory-answer-2'; }

  tea() {
    return '#radio-non-mandatory-answer-3';
  }

  teaLabel() { return '#label-radio-non-mandatory-answer-3'; }

  other() {
    return '#radio-non-mandatory-answer-4';
  }

  otherLabel() { return '#label-radio-non-mandatory-answer-4'; }

  otherText() {
    return '#other-answer-non-mandatory';
  }

}
module.exports = new RadioNonMandatoryPage();
