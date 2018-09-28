// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  comparison1Answer(index = 0) { return '#comparison-1-answer-' + index + '-answer'; }

  comparison1AnswerEdit(index = 0) { return '[data-qa="comparison-1-answer-' + index + '-edit"]'; }

  comparison2Answer(index = 0) { return '#comparison-2-answer-' + index + '-answer'; }

  comparison2AnswerEdit(index = 0) { return '[data-qa="comparison-2-answer-' + index + '-edit"]'; }

  skipGroupTitle(index = 0) { return '#skip-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
