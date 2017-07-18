// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SecurityCodePage extends QuestionPage {

  constructor() {
    super('security-code');
  }

  answer() {
    return '#security-code-answer';
  }

  answerLabel() { return '#label-security-code-answer'; }

}
module.exports = new SecurityCodePage();
