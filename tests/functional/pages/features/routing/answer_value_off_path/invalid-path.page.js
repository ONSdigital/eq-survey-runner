// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class InvalidPathPage extends QuestionPage {

  constructor() {
    super('invalid-path');
  }

  answer() {
    return '#invalid-path-answer';
  }

  answerLabel() { return '#label-invalid-path-answer'; }

}
module.exports = new InvalidPathPage();
