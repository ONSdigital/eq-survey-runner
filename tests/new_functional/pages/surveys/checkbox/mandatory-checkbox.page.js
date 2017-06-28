// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class MandatoryCheckboxPage extends QuestionPage {

  constructor() {
    super('mandatory-checkbox');
  }

  none() {
    return '#mandatory-checkbox-answer-0';
  }

  noneLabel() { return '#label-mandatory-checkbox-answer-0'; }

  cheese() {
    return '#mandatory-checkbox-answer-1';
  }

  cheeseLabel() { return '#label-mandatory-checkbox-answer-1'; }

  ham() {
    return '#mandatory-checkbox-answer-2';
  }

  hamLabel() { return '#label-mandatory-checkbox-answer-2'; }

  pineapple() {
    return '#mandatory-checkbox-answer-3';
  }

  pineappleLabel() { return '#label-mandatory-checkbox-answer-3'; }

  tuna() {
    return '#mandatory-checkbox-answer-4';
  }

  tunaLabel() { return '#label-mandatory-checkbox-answer-4'; }

  pepperoni() {
    return '#mandatory-checkbox-answer-5';
  }

  pepperoniLabel() { return '#label-mandatory-checkbox-answer-5'; }

  other() {
    return '#mandatory-checkbox-answer-6';
  }

  otherLabel() { return '#label-mandatory-checkbox-answer-6'; }

  otherText() {
    return '#other-answer-mandatory';
  }

}
module.exports = new MandatoryCheckboxPage();
