// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  lastName(index = 0) { return '#last-name-' + index + '-answer'; }

  lastNameEdit(index = 0) { return '[data-qa="last-name-' + index + '-edit"]'; }

  multipleQuestionsGroupTitle(index = 0) { return '#multiple-questions-group-' + index; }

  groupLessThan2Answer(index = 0) { return '#group-less-than-2-answer-' + index + '-answer'; }

  groupLessThan2AnswerEdit(index = 0) { return '[data-qa="group-less-than-2-answer-' + index + '-edit"]'; }

  groupLessThan2Title(index = 0) { return '#group-less-than-2-' + index; }

  groupEqual2Answer(index = 0) { return '#group-equal-2-answer-' + index + '-answer'; }

  groupEqual2AnswerEdit(index = 0) { return '[data-qa="group-equal-2-answer-' + index + '-edit"]'; }

  groupEqual2Title(index = 0) { return '#group-equal-2-' + index; }

  groupGreaterThan2Answer(index = 0) { return '#group-greater-than-2-answer-' + index + '-answer'; }

  groupGreaterThan2AnswerEdit(index = 0) { return '[data-qa="group-greater-than-2-answer-' + index + '-edit"]'; }

  groupGreaterThan2Title(index = 0) { return '#group-greater-than-2-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
