// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class RadioMandatoryPage extends QuestionPage {

  constructor() {
    super('radio-mandatory');
  }

  toast() {
    return '#radio-mandatory-answer-0';
  }

  toastLabel() { return '#label-radio-mandatory-answer-0'; }

  other() {
    return '#radio-mandatory-answer-1';
  }

  otherLabel() { return '#label-radio-mandatory-answer-1'; }

  otherText() {
    return '#other-answer-mandatory';
  }

}
module.exports = new RadioMandatoryPage();
