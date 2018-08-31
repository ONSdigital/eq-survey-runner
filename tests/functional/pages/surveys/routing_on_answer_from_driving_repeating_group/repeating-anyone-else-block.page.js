// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class RepeatingAnyoneElseBlockPage extends QuestionPage {

  constructor() {
    super('repeating-anyone-else-block');
  }

  yes() {
    return '#repeating-anyone-else-0';
  }

  yesLabel() { return '#label-repeating-anyone-else-0'; }

  no() {
    return '#repeating-anyone-else-1';
  }

  noLabel() { return '#label-repeating-anyone-else-1'; }

}
module.exports = new RepeatingAnyoneElseBlockPage();
