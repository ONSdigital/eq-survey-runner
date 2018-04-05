// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RepeatingBlock3Page extends QuestionPage {

  constructor() {
    super('repeating-block-3');
  }

  yes() {
    return '#confirm-answer-0';
  }

  yesLabel() { return '#label-confirm-answer-0'; }

  no() {
    return '#confirm-answer-1';
  }

  noLabel() { return '#label-confirm-answer-1'; }

}
module.exports = new RepeatingBlock3Page();
