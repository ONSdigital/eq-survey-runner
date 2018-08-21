// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SkipFourthBlockPage extends QuestionPage {

  constructor() {
    super('skip-fourth-block');
  }

  yes() {
    return '#skip-fourth-block-answer-0';
  }

  yesLabel() { return '#label-skip-fourth-block-answer-0'; }

  no() {
    return '#skip-fourth-block-answer-1';
  }

  noLabel() { return '#label-skip-fourth-block-answer-1'; }

}
module.exports = new SkipFourthBlockPage();
