// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const CalculatedSummaryPage = require('../../calculated-summary.page');

class UnitTotalPlaybackPage extends CalculatedSummaryPage {

  constructor() {
    super('unit-total-playback');
  }

  secondNumberAnswerUnitTotal(index = 0) { return '#second-number-answer-unit-total-' + index + '-answer'; }

  secondNumberAnswerUnitTotalEdit(index = 0) { return '[data-qa="second-number-answer-unit-total-' + index + '-edit"]'; }

  secondNumberAnswerUnitTotalLabel(index = 0) { return '#second-number-answer-unit-total-' + index + '-label'; }

  thirdNumberAnswerUnitTotal(index = 0) { return '#third-number-answer-unit-total-' + index + '-answer'; }

  thirdNumberAnswerUnitTotalEdit(index = 0) { return '[data-qa="third-number-answer-unit-total-' + index + '-edit"]'; }

  thirdNumberAnswerUnitTotalLabel(index = 0) { return '#third-number-answer-unit-total-' + index + '-label'; }

}
module.exports = new UnitTotalPlaybackPage();
