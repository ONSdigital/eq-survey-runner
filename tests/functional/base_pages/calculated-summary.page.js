const QuestionPage = require('./question.page');

class CalculatedSummaryPage extends QuestionPage {

  constructor(pageName) {
    super(pageName);
  }

  calculatedSummaryTitle() { return '[data-qa="calculated-summary-title"]'; }

  calculatedSummaryQuestion() { return '#calculated-summary-question'; }

  calculatedSummaryAnswer() { return '#calculated-summary-answer-answer'; }

}

module.exports = CalculatedSummaryPage;
