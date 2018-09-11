// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  comparison1Answer() { return '#comparison-1-answer-answer'; }

  comparison1AnswerEdit() { return '[data-qa="comparison-1-answer-edit"]'; }

  comparison2Answer() { return '#comparison-2-answer-answer'; }

  comparison2AnswerEdit() { return '[data-qa="comparison-2-answer-edit"]'; }

  skipGroupTitle() { return '#skip-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
