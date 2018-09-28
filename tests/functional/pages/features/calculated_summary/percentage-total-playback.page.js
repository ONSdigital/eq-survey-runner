// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const CalculatedSummaryPage = require('../../calculated-summary.page');

class PercentageTotalPlaybackPage extends CalculatedSummaryPage {

  constructor() {
    super('percentage-total-playback');
  }

  fifthPercentAnswer(index = 0) { return '#fifth-percent-answer-' + index + '-answer'; }

  fifthPercentAnswerEdit(index = 0) { return '[data-qa="fifth-percent-answer-' + index + '-edit"]'; }

  fifthPercentAnswerLabel(index = 0) { return '#fifth-percent-answer-' + index + '-label'; }

  sixthPercentAnswer(index = 0) { return '#sixth-percent-answer-' + index + '-answer'; }

  sixthPercentAnswerEdit(index = 0) { return '[data-qa="sixth-percent-answer-' + index + '-edit"]'; }

  sixthPercentAnswerLabel(index = 0) { return '#sixth-percent-answer-' + index + '-label'; }

}
module.exports = new PercentageTotalPlaybackPage();
