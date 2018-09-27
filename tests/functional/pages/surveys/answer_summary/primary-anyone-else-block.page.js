// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class PrimaryAnyoneElseBlockPage extends QuestionPage {

  constructor() {
    super('primary-anyone-else-block');
  }

  yes() {
    return '#primary-anyone-else-0';
  }

  yesLabel() { return '#label-primary-anyone-else-0'; }

  no() {
    return '#primary-anyone-else-1';
  }

  noLabel() { return '#label-primary-anyone-else-1'; }

}
module.exports = new PrimaryAnyoneElseBlockPage();
