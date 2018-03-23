// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class ConfirmZeroEmployeesBlockPage extends QuestionPage {

  constructor() {
    super('confirm-zero-employees-block');
  }

  yes() {
    return '#confirm-zero-employees-answer-0';
  }

  yesLabel() { return '#label-confirm-zero-employees-answer-0'; }

  no() {
    return '#confirm-zero-employees-answer-1';
  }

  noLabel() { return '#label-confirm-zero-employees-answer-1'; }

}
module.exports = new ConfirmZeroEmployeesBlockPage();
