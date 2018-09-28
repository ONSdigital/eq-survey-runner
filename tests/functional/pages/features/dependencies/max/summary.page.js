// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  maxAnswer(index = 0) { return '#max-answer-' + index + '-answer'; }

  maxAnswerEdit(index = 0) { return '[data-qa="max-answer-' + index + '-edit"]'; }

  dependent1(index = 0) { return '#dependent-1-' + index + '-answer'; }

  dependent1Edit(index = 0) { return '[data-qa="dependent-1-' + index + '-edit"]'; }

  groupTitle(index = 0) { return '#group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
