// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  initialChoiceAnswer(index = 0) { return '#initial-choice-answer-' + index + '-answer'; }

  initialChoiceAnswerEdit(index = 0) { return '[data-qa="initial-choice-answer-' + index + '-edit"]'; }

  initialChoiceQuestion(index = 0) { return '#initial-choice-question-' + index; }

  invalidPathAnswer(index = 0) { return '#invalid-path-answer-' + index + '-answer'; }

  invalidPathAnswerEdit(index = 0) { return '[data-qa="invalid-path-answer-' + index + '-edit"]'; }

  invalidPathQuestion(index = 0) { return '#invalid-path-question-' + index; }

  validPathAnswer(index = 0) { return '#valid-path-answer-' + index + '-answer'; }

  validPathAnswerEdit(index = 0) { return '[data-qa="valid-path-answer-' + index + '-edit"]'; }

  validPathQuestion(index = 0) { return '#valid-path-question-' + index; }

  groupTitle(index = 0) { return '#group-' + index; }

}
module.exports = new SummaryPage();
