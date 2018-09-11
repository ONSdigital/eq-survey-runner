// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  routeComparison1Answer() { return '#route-comparison-1-answer-answer'; }

  routeComparison1AnswerEdit() { return '[data-qa="route-comparison-1-answer-edit"]'; }

  routeComparison2Answer() { return '#route-comparison-2-answer-answer'; }

  routeComparison2AnswerEdit() { return '[data-qa="route-comparison-2-answer-edit"]'; }

  routeGroupTitle() { return '#route-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
