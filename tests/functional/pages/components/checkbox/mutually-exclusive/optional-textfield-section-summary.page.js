// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalTextfieldSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-textfield-section-summary');
  }

  textfieldAnswer(index = 0) { return '#textfield-answer-' + index + '-answer'; }

  textfieldAnswerEdit(index = 0) { return '[data-qa="textfield-answer-' + index + '-edit"]'; }

  textfieldExclusiveAnswer(index = 0) { return '#textfield-exclusive-answer-' + index + '-answer'; }

  textfieldExclusiveAnswerEdit(index = 0) { return '[data-qa="textfield-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveTextfieldQuestion(index = 0) { return '#mutually-exclusive-textfield-question-' + index; }

  mutuallyExclusiveTextfieldGroupTitle(index = 0) { return '#mutually-exclusive-textfield-group-' + index; }

  mutuallyExclusiveTextfieldSectionSummaryTitle(index = 0) { return '#mutually-exclusive-textfield-section-summary-' + index; }

}
module.exports = new OptionalTextfieldSectionSummaryPage();
