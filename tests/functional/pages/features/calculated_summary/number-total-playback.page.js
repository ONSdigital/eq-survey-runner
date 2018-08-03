// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../surveys/question.page');

class NumberTotalPlaybackPage extends QuestionPage {

  constructor() {
    super('number-total-playback');
  }

  fifthNumberAnswer() { return '#fifth-number-answer-answer'; }

  fifthNumberAnswerEdit() { return '[data-qa="fifth-number-answer-edit"]'; }

  sixthNumberAnswer() { return '#sixth-number-answer-answer'; }

  sixthNumberAnswerEdit() { return '[data-qa="sixth-number-answer-edit"]'; }

  calculatedSummaryTitle() { return '[data-qa="calculated-summary-title"]'; }

  calculatedSummaryQuestion() { return '#calculated-summary-question'; }

  calculatedSummaryAnswer() { return '#calculated-summary-answer-answer'; }

  groupTitle() { return '#group'; }

}
module.exports = new NumberTotalPlaybackPage();
