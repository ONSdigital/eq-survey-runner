// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  routeComparison1Answer(index = 0) { return '#route-comparison-1-answer-' + index + '-answer'; }

  routeComparison1AnswerEdit(index = 0) { return '[data-qa="route-comparison-1-answer-' + index + '-edit"]'; }

  routeComparison2Answer(index = 0) { return '#route-comparison-2-answer-' + index + '-answer'; }

  routeComparison2AnswerEdit(index = 0) { return '[data-qa="route-comparison-2-answer-' + index + '-edit"]'; }

  routeGroupTitle(index = 0) { return '#route-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
