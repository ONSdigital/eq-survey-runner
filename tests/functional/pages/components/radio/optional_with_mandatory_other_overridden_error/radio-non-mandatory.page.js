// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class RadioNonMandatoryPage extends QuestionPage {

  constructor() {
    super('radio-non-mandatory');
  }

  toast() {
    return '#radio-non-mandatory-answer-0';
  }

  toastLabel() { return '#label-radio-non-mandatory-answer-0'; }

  other() {
    return '#radio-non-mandatory-answer-1';
  }

  otherLabel() { return '#label-radio-non-mandatory-answer-1'; }

  otherText() {
    return '#other-answer-non-mandatory';
  }

}
module.exports = new RadioNonMandatoryPage();
