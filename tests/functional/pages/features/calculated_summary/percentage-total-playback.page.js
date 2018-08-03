// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class CurrencyTotalPlaybackPage extends QuestionPage {

  constructor() {
    super('currency-total-playback');
  }

  fifthPercentAnswer() { return '#fifth-percent-answer-answer'; }

  fifthPercentAnswerEdit() { return '[data-qa="fifth-percent-answer-edit"]'; }

  sixthPercentAnswer() { return '#sixth-percent-answer-answer'; }

  sixthPercentAnswerEdit() { return '[data-qa="sixth-percent-answer-edit"]'; }

  calculatedSummaryTitle() { return '[data-qa="calculated-summary-title"]'; }

  calculatedSummaryQuestion() { return '#calculated-summary-question'; }

  calculatedSummaryAnswer() { return '#calculated-summary-answer-answer'; }

  groupTitle() { return '#group'; }

}
module.exports = new CurrencyTotalPlaybackPage();
