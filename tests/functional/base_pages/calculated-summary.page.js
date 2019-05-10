const QuestionPage = require('./question.page');

class CalculatedSummaryPage extends QuestionPage {

  constructor(pageName) {
    super(pageName);
  }

  calculatedSummaryTitle() { return '[data-qa="calculated-summary-title"]'; }

  calculatedSummaryQuestion() { return '[data-qa=calculated-summary-question]'; }

  calculatedSummaryAnswer() { return '[data-qa=calculated-summary-answer]'; }

}

module.exports = CalculatedSummaryPage;
