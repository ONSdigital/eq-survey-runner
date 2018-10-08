// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalDurationSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-duration-section-summary');
  }

  durationAnswer(index = 0) { return '#duration-answer-' + index + '-answer'; }

  durationAnswerEdit(index = 0) { return '[data-qa="duration-answer-' + index + '-edit"]'; }

  durationExclusiveAnswer(index = 0) { return '#duration-exclusive-answer-' + index + '-answer'; }

  durationExclusiveAnswerEdit(index = 0) { return '[data-qa="duration-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveDurationQuestion(index = 0) { return '#mutually-exclusive-duration-question-' + index; }

  mutuallyExclusiveDurationGroupTitle(index = 0) { return '#mutually-exclusive-duration-group-' + index; }

  mutuallyExclusiveDurationSectionSummaryTitle(index = 0) { return '#mutually-exclusive-duration-section-summary-' + index; }

}
module.exports = new OptionalDurationSectionSummaryPage();
