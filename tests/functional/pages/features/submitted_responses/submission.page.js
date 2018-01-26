// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  radioAnswer() { return '#radio-answer-answer'; }

  radioAnswerEdit() { return '[data-qa="radio-answer-edit"]'; }

  otherAnswerMandatory() { return '#other-answer-mandatory-answer'; }

  otherAnswerMandatoryEdit() { return '[data-qa="other-answer-mandatory-edit"]'; }

  testCurrency() { return '#test-currency-answer'; }

  testCurrencyEdit() { return '[data-qa="test-currency-edit"]'; }

  squareKilometres() { return '#square-kilometres-answer'; }

  squareKilometresEdit() { return '[data-qa="square-kilometres-edit"]'; }

  testDecimal() { return '#test-decimal-answer'; }

  testDecimalEdit() { return '[data-qa="test-decimal-edit"]'; }

}
module.exports = new SummaryPage();
