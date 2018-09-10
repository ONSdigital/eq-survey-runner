// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../surveys/../question.page');

class MemberSummaryBlockPage extends QuestionPage {

  constructor() {
    super('member-summary-block');
  }

  primaryNameQuestion(index = 0) { return '#primary-name-question-' + index; }

  primaryName(index = 0) { return '#primary-name-' + index + '-answer'; }

  primaryNameEdit(index = 0) { return '[data-qa="primary-name-' + index + '-edit"]'; }

  primaryGroupTitle(index = 0) { return '#primary-group-' + index; }

  repeatingAnyoneElseQuestion(index = 0) { return '#repeating-anyone-else-question-' + index; }

  repeatingAnyoneElse(index = 0) { return '#repeating-anyone-else-' + index + '-answer'; }

  repeatingAnyoneElseEdit(index = 0) { return '[data-qa="repeating-anyone-else-' + index + '-edit"]'; }

  repeatingNameQuestion(index = 0) { return '#repeating-name-question-' + index; }

  repeatingName(index = 0) { return '#repeating-name-' + index + '-answer'; }

  repeatingNameEdit(index = 0) { return '[data-qa="repeating-name-' + index + '-edit"]'; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  householdSummaryGroupTitle(index = 0) { return '#household-summary-group-' + index; }

  firstNumberQuestion(index = 0) { return '#first-number-question-' + index; }

  firstNumberAnswer(index = 0) { return '#first-number-answer-' + index + '-answer'; }

  firstNumberAnswerEdit(index = 0) { return '[data-qa="first-number-answer-' + index + '-edit"]'; }

  secondNumberQuestion(index = 0) { return '#second-number-question-' + index; }

  secondNumberAnswer(index = 0) { return '#second-number-answer-' + index + '-answer'; }

  secondNumberAnswerEdit(index = 0) { return '[data-qa="second-number-answer-' + index + '-edit"]'; }

  memberGroupTitle(index = 0) { return '#member-group-' + index; }

  memberSummaryGroupTitle(index = 0) { return '#member-summary-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new MemberSummaryBlockPage();
