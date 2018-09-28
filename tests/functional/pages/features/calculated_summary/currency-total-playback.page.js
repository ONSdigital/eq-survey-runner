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

  secondNumberAnswerAlsoInTotal(index = 0) { return '#second-number-answer-also-in-total-' + index + '-answer'; }

  secondNumberAnswerAlsoInTotalEdit(index = 0) { return '[data-qa="second-number-answer-also-in-total-' + index + '-edit"]'; }

  secondNumberAnswerAlsoInTotalLabel(index = 0) { return '#second-number-answer-also-in-total-' + index + '-label'; }

  thirdNumberAnswer(index = 0) { return '#third-number-answer-' + index + '-answer'; }

  thirdNumberAnswerEdit(index = 0) { return '[data-qa="third-number-answer-' + index + '-edit"]'; }

  thirdNumberAnswerLabel(index = 0) { return '#third-number-answer-' + index + '-label'; }

  fourthNumberAnswer(index = 0) { return '#fourth-number-answer-' + index + '-answer'; }

  fourthNumberAnswerEdit(index = 0) { return '[data-qa="fourth-number-answer-' + index + '-edit"]'; }

  fourthNumberAnswerLabel(index = 0) { return '#fourth-number-answer-' + index + '-label'; }

  fourthNumberAnswerAlsoInTotal(index = 0) { return '#fourth-number-answer-also-in-total-' + index + '-answer'; }

  fourthNumberAnswerAlsoInTotalEdit(index = 0) { return '[data-qa="fourth-number-answer-also-in-total-' + index + '-edit"]'; }

  fourthNumberAnswerAlsoInTotalLabel(index = 0) { return '#fourth-number-answer-also-in-total-' + index + '-label'; }

}
module.exports = new CurrencyTotalPlaybackPage();
