// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SandwichBlockPage extends QuestionPage {

  constructor() {
    super('sandwich-block');
  }

  ham() {
    return '#sandwich-answer-0';
  }

  hamLabel() { return '#label-sandwich-answer-0'; }

  tuna() {
    return '#sandwich-answer-1';
  }

  tunaLabel() { return '#label-sandwich-answer-1'; }

}
module.exports = new SandwichBlockPage();
