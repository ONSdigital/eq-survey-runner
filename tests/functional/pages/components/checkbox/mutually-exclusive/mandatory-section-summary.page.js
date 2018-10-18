// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class MandatorySectionSummaryPage extends QuestionPage {

  constructor() {
    super('mandatory-section-summary');
  }

  checkboxAnswer(index = 0) { return '#checkbox-answer-' + index + '-answer'; }

  checkboxAnswerEdit(index = 0) { return '[data-qa="checkbox-answer-' + index + '-edit"]'; }

  checkboxExclusiveAnswer(index = 0) { return '#checkbox-exclusive-answer-' + index + '-answer'; }

  checkboxExclusiveAnswerEdit(index = 0) { return '[data-qa="checkbox-exclusive-answer-' + index + '-edit"]'; }

  checkboxChildOtherAnswer(index = 0) { return '#checkbox-child-other-answer-' + index + '-answer'; }

  checkboxChildOtherAnswerEdit(index = 0) { return '[data-qa="checkbox-child-other-answer-' + index + '-edit"]'; }

}
module.exports = new MandatorySectionSummaryPage();
