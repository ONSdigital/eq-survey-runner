// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RadioMandatoryPage extends QuestionPage {

  constructor() {
    super('radio-mandatory');
  }

  none() {
    return '#radio-mandatory-answer-0';
  }

  noneLabel() { return '#label-radio-mandatory-answer-0'; }

  bacon() {
    return '#radio-mandatory-answer-1';
  }

  baconLabel() { return '#label-radio-mandatory-answer-1'; }

  eggs() {
    return '#radio-mandatory-answer-2';
  }

  eggsLabel() { return '#label-radio-mandatory-answer-2'; }

  sausage() {
    return '#radio-mandatory-answer-3';
  }

  sausageLabel() { return '#label-radio-mandatory-answer-3'; }

  other() {
    return '#radio-mandatory-answer-4';
  }

  otherLabel() { return '#label-radio-mandatory-answer-4'; }

  otherText() {
    return '#other-answer-mandatory';
  }

}
module.exports = new RadioMandatoryPage();
