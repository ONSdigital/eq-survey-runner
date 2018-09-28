// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const CalculatedSummaryPage = require('../../calculated-summary.page');

class NumberTotalPlaybackPage extends CalculatedSummaryPage {

  constructor() {
    super('number-total-playback');
  }

  fifthNumberAnswer(index = 0) { return '#fifth-number-answer-' + index + '-answer'; }

  fifthNumberAnswerEdit(index = 0) { return '[data-qa="fifth-number-answer-' + index + '-edit"]'; }

  fifthNumberAnswerLabel(index = 0) { return '#fifth-number-answer-' + index + '-label'; }

  sixthNumberAnswer(index = 0) { return '#sixth-number-answer-' + index + '-answer'; }

  sixthNumberAnswerEdit(index = 0) { return '[data-qa="sixth-number-answer-' + index + '-edit"]'; }

  sixthNumberAnswerLabel(index = 0) { return '#sixth-number-answer-' + index + '-label'; }

}
module.exports = new NumberTotalPlaybackPage();
