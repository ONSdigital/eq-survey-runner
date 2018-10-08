// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalTextareaSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-textarea-section-summary');
  }

  textareaAnswer(index = 0) { return '#textarea-answer-' + index + '-answer'; }

  textareaAnswerEdit(index = 0) { return '[data-qa="textarea-answer-' + index + '-edit"]'; }

  textareaExclusiveAnswer(index = 0) { return '#textarea-exclusive-answer-' + index + '-answer'; }

  textareaExclusiveAnswerEdit(index = 0) { return '[data-qa="textarea-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveTextareaQuestion(index = 0) { return '#mutually-exclusive-textarea-question-' + index; }

  mutuallyExclusiveTextareaGroupTitle(index = 0) { return '#mutually-exclusive-textarea-group-' + index; }

  mutuallyExclusiveTextareaSectionSummaryTitle(index = 0) { return '#mutually-exclusive-textarea-section-summary-' + index; }

}
module.exports = new OptionalTextareaSectionSummaryPage();
