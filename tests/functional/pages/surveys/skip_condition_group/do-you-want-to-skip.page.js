// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class DoYouWantToSkipPage extends QuestionPage {

  constructor() {
    super('do-you-want-to-skip');
  }

  yes() {
    return '#do-you-want-to-skip-answer-0';
  }

  yesLabel() { return '#label-do-you-want-to-skip-answer-0'; }

  no() {
    return '#do-you-want-to-skip-answer-1';
  }

  noLabel() { return '#label-do-you-want-to-skip-answer-1'; }

}
module.exports = new DoYouWantToSkipPage();
