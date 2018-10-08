// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class OptionalDropdownSectionSummaryPage extends QuestionPage {

  constructor() {
    super('optional-dropdown-section-summary');
  }

  dropdownAnswer(index = 0) { return '#dropdown-answer-' + index + '-answer'; }

  dropdownAnswerEdit(index = 0) { return '[data-qa="dropdown-answer-' + index + '-edit"]'; }

  dropdownExclusiveAnswer(index = 0) { return '#dropdown-exclusive-answer-' + index + '-answer'; }

  dropdownExclusiveAnswerEdit(index = 0) { return '[data-qa="dropdown-exclusive-answer-' + index + '-edit"]'; }

  mutuallyExclusiveDropdownQuestion(index = 0) { return '#mutually-exclusive-dropdown-question-' + index; }

  mutuallyExclusiveDropdownGroupTitle(index = 0) { return '#mutually-exclusive-dropdown-group-' + index; }

  mutuallyExclusiveDropdownSectionSummaryTitle(index = 0) { return '#mutually-exclusive-dropdown-section-summary-' + index; }

}
module.exports = new OptionalDropdownSectionSummaryPage();
