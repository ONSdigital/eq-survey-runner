// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  repeatingComparison1Answer(index = 0) { return '#repeating-comparison-1-answer-' + index + '-answer'; }

  repeatingComparison1AnswerEdit(index = 0) { return '[data-qa="repeating-comparison-1-answer-' + index + '-edit"]'; }

  repeatingComparison2Answer(index = 0) { return '#repeating-comparison-2-answer-' + index + '-answer'; }

  repeatingComparison2AnswerEdit(index = 0) { return '[data-qa="repeating-comparison-2-answer-' + index + '-edit"]'; }

  repeatingComparisonTitle(index = 0) { return '#repeating-comparison-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
