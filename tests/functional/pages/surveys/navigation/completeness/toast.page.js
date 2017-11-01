// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class ToastPage extends QuestionPage {

  constructor() {
    super('toast');
  }

  yes() {
    return '#toast-answer-0';
  }

  yesLabel() { return '#label-toast-answer-0'; }

  no() {
    return '#toast-answer-1';
  }

  noLabel() { return '#label-toast-answer-1'; }

}
module.exports = new ToastPage();
