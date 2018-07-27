// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class CurrencyTotalPlaybackPage extends QuestionPage {

  constructor() {
    super('currency-total-playback');
  }

  secondNumberAnswerUnitTotal() { return '#second-number-answer-unit-total-answer'; }

  secondNumberAnswerUnitTotalEdit() { return '[data-qa="second-number-answer-unit-total-edit"]'; }

  thirdNumberAnswerUnitTotal() { return '#third-number-answer-unit-total-answer'; }

  thirdNumberAnswerUnitTotalEdit() { return '[data-qa="third-number-answer-unit-total-edit"]'; }

  calculatedSummaryTitle() { return '[data-qa="calculated-summary-title"]'; }

  calculatedSummaryQuestion() { return '#calculated-summary-question'; }

  calculatedSummaryAnswer() { return '#calculated-summary-answer-answer'; }

  groupTitle() { return '#group'; }

}
module.exports = new CurrencyTotalPlaybackPage();
