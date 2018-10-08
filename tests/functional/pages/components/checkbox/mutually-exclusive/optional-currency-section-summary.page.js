// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalCurrencySectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-currency-section-summary');
  }

  currencyAnswer(index = 0) { return '#currency-answer-' + index + '-answer'; }

  currencyAnswerEdit(index = 0) { return '[data-qa="currency-answer-' + index + '-edit"]'; }

  currencyExclusiveAnswer(index = 0) { return '#currency-exclusive-answer-' + index + '-answer'; }

  currencyExclusiveAnswerEdit(index = 0) { return '[data-qa="currency-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveCurrencyQuestion(index = 0) { return '#mutually-exclusive-currency-question-' + index; }

  mutuallyExclusiveCurrencyGroupTitle(index = 0) { return '#mutually-exclusive-currency-group-' + index; }

  mutuallyExclusiveCurrencySectionSummaryTitle(index = 0) { return '#mutually-exclusive-currency-section-summary-' + index; }


}
module.exports = new OptionalCurrencySectionSummaryPage();
