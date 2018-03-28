// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  minAnswer() { return '#min-answer-answer'; }

  minAnswerEdit() { return '[data-qa="min-answer-edit"]'; }

  dependent1() { return '#dependent-1-answer'; }

  dependent1Edit() { return '[data-qa="dependent-1-edit"]'; }

  groupTitle() { return '#group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
