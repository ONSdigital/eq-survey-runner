// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class NonMandatoryCheckboxPage extends QuestionPage {

  constructor() {
    super('non-mandatory-checkbox');
  }

  none() {
    return '#non-mandatory-checkbox-answer-0';
  }

  cheese() {
    return '#non-mandatory-checkbox-answer-1';
  }

  ham() {
    return '#non-mandatory-checkbox-answer-2';
  }

  pineapple() {
    return '#non-mandatory-checkbox-answer-3';
  }

  tuna() {
    return '#non-mandatory-checkbox-answer-4';
  }

  pepperoni() {
    return '#non-mandatory-checkbox-answer-5';
  }

  other() {
    return '#non-mandatory-checkbox-answer-6';
  }

  otherText() {
    return '#other-answer-non-mandatory';
  }

}
module.exports = new NonMandatoryCheckboxPage();
