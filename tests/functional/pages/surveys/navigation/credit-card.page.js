// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class CreditCardPage extends QuestionPage {

  constructor() {
    super('credit-card');
  }

  answer() {
    return '#credit-card-answer';
  }

  answerLabel() { return '#label-credit-card-answer'; }

}
module.exports = new CreditCardPage();
