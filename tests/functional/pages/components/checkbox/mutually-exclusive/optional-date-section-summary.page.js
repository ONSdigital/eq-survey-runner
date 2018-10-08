// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalDateSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-date-section-summary');
  }

  dateAnswer(index = 0) { return '#date-answer-' + index + '-answer'; }

  dateAnswerEdit(index = 0) { return '[data-qa="date-answer-' + index + '-edit"]'; }

  dateExclusiveAnswer(index = 0) { return '#date-exclusive-answer-' + index + '-answer'; }

  dateExclusiveAnswerEdit(index = 0) { return '[data-qa="date-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveDateQuestion(index = 0) { return '#mutually-exclusive-date-question-' + index; }

  mutuallyExclusiveDateGroupTitle(index = 0) { return '#mutually-exclusive-date-group-' + index; }

  mutuallyExclusiveDateSectionSummaryTitle(index = 0) { return '#mutually-exclusive-date-section-summary-' + index; }

}
module.exports = new OptionalDateSectionSummaryPage();
