// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MandatoryCheckboxPage extends QuestionPage {

  constructor() {
    super('mandatory-checkbox');
  }

  cheese() {
    return '#mandatory-checkbox-answer-0';
  }

  cheeseLabel() { return '#label-mandatory-checkbox-answer-0'; }

  ham() {
    return '#mandatory-checkbox-answer-1';
  }

  hamLabel() { return '#label-mandatory-checkbox-answer-1'; }

  pineapple() {
    return '#mandatory-checkbox-answer-2';
  }

  pineappleLabel() { return '#label-mandatory-checkbox-answer-2'; }

  tuna() {
    return '#mandatory-checkbox-answer-3';
  }

  tunaLabel() { return '#label-mandatory-checkbox-answer-3'; }

  pepperoni() {
    return '#mandatory-checkbox-answer-4';
  }

  pepperoniLabel() { return '#label-mandatory-checkbox-answer-4'; }

  other() {
    return '#mandatory-checkbox-answer-5';
  }

  otherLabel() { return '#label-mandatory-checkbox-answer-5'; }

  otherText() {
    return '#other-answer-mandatory';
  }

  none() {
    return '#mandatory-checkbox-answer-6';
  }

  noneLabel() { return '#label-mandatory-checkbox-answer-6'; }

}
module.exports = new MandatoryCheckboxPage();
