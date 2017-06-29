// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class DoYouWantToSkipPage extends QuestionPage {

  constructor() {
    super('do-you-want-to-skip');
  }

  firstYes() {
    return '#do-you-want-to-skip-first-answer-0';
  }

  firstNo() {
    return '#do-you-want-to-skip-first-answer-1';
  }

  secondYes() {
    return '#do-you-want-to-skip-second-answer-0';
  }

  secondNo() {
    return '#do-you-want-to-skip-second-answer-1';
  }

}
module.exports = new DoYouWantToSkipPage();
