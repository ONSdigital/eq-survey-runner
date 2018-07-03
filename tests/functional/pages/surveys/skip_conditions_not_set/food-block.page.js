// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class FoodBlockPage extends QuestionPage {

  constructor() {
    super('food-block');
  }

  bacon() {
    return '#food-answer-0';
  }

  baconLabel() { return '#label-food-answer-0'; }

  eggs() {
    return '#food-answer-1';
  }

  eggsLabel() { return '#label-food-answer-1'; }

}
module.exports = new FoodBlockPage();
