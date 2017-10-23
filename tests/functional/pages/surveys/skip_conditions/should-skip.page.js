// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class ShouldSkipPage extends QuestionPage {

  constructor() {
    super('should-skip');
  }

  skippedOneYes() {
    return '#skipped-answer-one-0';
  }

  skippedOneNo() {
    return '#skipped-answer-one-1';
  }

  skipTwoYes() {
    return '#skip-answer-two-0';
  }

  skipTwoNo() {
    return '#skip-answer-two-1';
  }

}
module.exports = new ShouldSkipPage();
