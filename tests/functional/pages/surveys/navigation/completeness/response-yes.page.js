// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class ResponseYesPage extends QuestionPage {

  constructor() {
    super('response-yes');
  }

  answer() {
    return '#response-yes-number-of-cups';
  }

  answerLabel() { return '#label-response-yes-number-of-cups'; }

}
module.exports = new ResponseYesPage();
