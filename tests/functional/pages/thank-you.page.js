const QuestionPage = require('./surveys/question.page');

class ThankYouPage extends QuestionPage {

  constructor() {
    super('thank-you');
  }

  viewSubmitted() {
    return '[data-qa="view-submission"]';
  }

  viewSubmissionExpired() {
    return '[data-qa="view-submission-expired"]';
  }

}
module.exports = new ThankYouPage();
