// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../../surveys/question.page');

class ToppingCheckboxPage extends QuestionPage {

  constructor() {
    super('topping-checkbox');
  }

  none() {
    return '#topping-checkbox-answer-0';
  }

  noneLabel() { return '#label-topping-checkbox-answer-0'; }

  cheese() {
    return '#topping-checkbox-answer-1';
  }

  cheeseLabel() { return '#label-topping-checkbox-answer-1'; }

  ham() {
    return '#topping-checkbox-answer-2';
  }

  hamLabel() { return '#label-topping-checkbox-answer-2'; }

  pineapple() {
    return '#topping-checkbox-answer-3';
  }

  pineappleLabel() { return '#label-topping-checkbox-answer-3'; }

  tuna() {
    return '#topping-checkbox-answer-4';
  }

  tunaLabel() { return '#label-topping-checkbox-answer-4'; }

  pepperoni() {
    return '#topping-checkbox-answer-5';
  }

  pepperoniLabel() { return '#label-topping-checkbox-answer-5'; }

  other() {
    return '#topping-checkbox-answer-6';
  }

  otherLabel() { return '#label-topping-checkbox-answer-6'; }

  otherText() {
    return '#other-answer-topping';
  }

}
module.exports = new ToppingCheckboxPage();
