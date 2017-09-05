// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RadioPage extends QuestionPage {

  constructor() {
    super('radio');
  }

  none() {
    return '#radio-answer-0';
  }

  noneLabel() { return '#label-radio-answer-0'; }

  bacon() {
    return '#radio-answer-1';
  }

  baconLabel() { return '#label-radio-answer-1'; }

  eggs() {
    return '#radio-answer-2';
  }

  eggsLabel() { return '#label-radio-answer-2'; }

  sausage() {
    return '#radio-answer-3';
  }

  sausageLabel() { return '#label-radio-answer-3'; }

  other() {
    return '#radio-answer-4';
  }

  otherLabel() { return '#label-radio-answer-4'; }

  otherText() {
    return '#other-answer-mandatory';
  }

}
module.exports = new RadioPage();
