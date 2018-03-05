// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

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

  summaryGroupTitle() { return '#summary-group'; }

  dessert() { return '#dessert-answer'; }

  dessertEdit() { return '[data-qa="dessert-edit"]'; }

  dessertGroupTitle() { return '#dessert-group'; }

}
module.exports = new SummaryPage();
