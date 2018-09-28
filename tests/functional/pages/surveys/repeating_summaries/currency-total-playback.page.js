// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const CalculatedSummaryPage = require('../../calculated-summary.page');

class CurrencyTotalPlaybackPage extends CalculatedSummaryPage {

  constructor() {
    super('currency-total-playback');
  }

  firstNumberAnswer(index = 0) { return '#first-number-answer-' + index + '-answer'; }

  firstNumberAnswerEdit(index = 0) { return '[data-qa="first-number-answer-' + index + '-edit"]'; }

  firstNumberAnswerLabel(index = 0) { return '#first-number-answer-' + index + '-label'; } 

  secondNumberAnswer(index = 0) { return '#second-number-answer-' + index + '-answer'; }

  secondNumberAnswerEdit(index = 0) { return '[data-qa="second-number-answer-' + index + '-edit"]'; }

  secondNumberAnswerLabel(index = 0) { return '#second-number-answer-' + index + '-label'; } 

}
module.exports = new CurrencyTotalPlaybackPage();
