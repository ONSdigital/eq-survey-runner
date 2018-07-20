// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  lastName() { return '#last-name-answer'; }

  lastNameEdit() { return '[data-qa="last-name-edit"]'; }

  multipleQuestionsGroupTitle() { return '#multiple-questions-group'; }

  groupLessThan2Answer() { return '#group-less-than-2-answer-answer'; }

  groupLessThan2AnswerEdit() { return '[data-qa="group-less-than-2-answer-edit"]'; }

  groupLessThan2Title() { return '#group-less-than-2'; }

  groupEqual2Answer() { return '#group-equal-2-answer-answer'; }

  groupEqual2AnswerEdit() { return '[data-qa="group-equal-2-answer-edit"]'; }

  groupEqual2Title() { return '#group-equal-2'; }

  groupGreaterThan2Answer() { return '#group-greater-than-2-answer-answer'; }

  groupGreaterThan2AnswerEdit() { return '[data-qa="group-greater-than-2-answer-edit"]'; }

  groupGreaterThan2Title() { return '#group-greater-than-2'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
