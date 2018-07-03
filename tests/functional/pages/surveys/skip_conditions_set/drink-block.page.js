// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class DrinkBlockPage extends QuestionPage {

  constructor() {
    super('drink-block');
  }

  tea() {
    return '#drink-answer-0';
  }

  teaLabel() { return '#label-drink-answer-0'; }

  coffee() {
    return '#drink-answer-1';
  }

  coffeeLabel() { return '#label-drink-answer-1'; }

}
module.exports = new DrinkBlockPage();
