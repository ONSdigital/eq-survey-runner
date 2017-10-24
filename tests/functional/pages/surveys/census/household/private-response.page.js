// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class PrivateResponsePage extends QuestionPage {

  constructor() {
    super('private-response');
  }

  noIDoNotWantToRequestAPersonalForm() {
    return '#private-response-answer-0';
  }

  yesIWantToRequestAPersonalForm() {
    return '#private-response-answer-1';
  }

}
module.exports = new PrivateResponsePage();
