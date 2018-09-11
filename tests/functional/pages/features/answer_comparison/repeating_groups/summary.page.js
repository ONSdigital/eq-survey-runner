// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  repeatingComparison1Answer() { return '#repeating-comparison-1-answer-answer'; }

  repeatingComparison1AnswerEdit() { return '[data-qa="repeating-comparison-1-answer-edit"]'; }

  repeatingComparison2Answer() { return '#repeating-comparison-2-answer-answer'; }

  repeatingComparison2AnswerEdit() { return '[data-qa="repeating-comparison-2-answer-edit"]'; }

  repeatingComparisonTitle() { return '#repeating-comparison'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
