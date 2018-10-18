// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MutuallyExclusiveCurrencyPage extends QuestionPage {

  constructor() {
    super('mutually-exclusive-currency');
  }

  currency() {
    return '#currency-answer';
  }

  currencyLabel() { return '#label-currency-answer'; }

  currencyExclusiveIPreferNotToSay() {
    return '#currency-exclusive-answer-0';
  }

  currencyExclusiveIPreferNotToSayLabel() { return '#label-currency-exclusive-answer-0'; }

}
module.exports = new MutuallyExclusiveCurrencyPage();
