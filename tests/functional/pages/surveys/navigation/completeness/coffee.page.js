// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class CoffeePage extends QuestionPage {

  constructor() {
    super('coffee');
  }

  yes() {
    return '#coffee-answer-0';
  }

  yesLabel() { return '#label-coffee-answer-0'; }

  no() {
    return '#coffee-answer-1';
  }

  noLabel() { return '#label-coffee-answer-1'; }

}
module.exports = new CoffeePage();
