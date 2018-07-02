const QuestionPage = require('./surveys/question.page');

class ThankYouPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  viewSubmissionText() {
    return '[data-qa="view-submission-text"]';
  }

}

module.exports = new ThankYouPage();
