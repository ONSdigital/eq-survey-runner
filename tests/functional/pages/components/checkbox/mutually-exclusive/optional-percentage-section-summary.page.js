// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalPercentageSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-percentage-section-summary');
  }

  percentageAnswer(index = 0) { return '#percentage-answer-' + index + '-answer'; }

  percentageAnswerEdit(index = 0) { return '[data-qa="percentage-answer-' + index + '-edit"]'; }

  percentageExclusiveAnswer(index = 0) { return '#percentage-exclusive-answer-' + index + '-answer'; }

  percentageExclusiveAnswerEdit(index = 0) { return '[data-qa="percentage-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusivePercentageQuestion(index = 0) { return '#mutually-exclusive-percentage-question-' + index; }

  mutuallyExclusivePercentageGroupTitle(index = 0) { return '#mutually-exclusive-percentage-group-' + index; }

  mutuallyExclusivePercentageSectionSummaryTitle(index = 0) { return '#mutually-exclusive-percentage-section-summary-' + index; }

}
module.exports = new OptionalPercentageSectionSummaryPage();
