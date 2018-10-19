// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  primaryName(index = 0) { return '#primary-name-' + index + '-answer'; }

  primaryNameEdit(index = 0) { return '[data-qa="primary-name-' + index + '-edit"]'; }

  primaryNameQuestion(index = 0) { return '#primary-name-question-' + index; }

  primaryLiveHere(index = 0) { return '#primary-live-here-' + index + '-answer'; }

  primaryLiveHereEdit(index = 0) { return '[data-qa="primary-live-here-' + index + '-edit"]'; }

  primaryLiveHereQuestion(index = 0) { return '#primary-live-here-question-' + index; }

  primaryGroupTitle(index = 0) { return '#primary-group-' + index; }

  repeatingAnyoneElse(index = 0) { return '#repeating-anyone-else-' + index + '-answer'; }

  repeatingAnyoneElseEdit(index = 0) { return '[data-qa="repeating-anyone-else-' + index + '-edit"]'; }

  repeatingAnyoneElseQuestion(index = 0) { return '#repeating-anyone-else-question-' + index; }

  repeatingName(index = 0) { return '#repeating-name-' + index + '-answer'; }

  repeatingNameEdit(index = 0) { return '[data-qa="repeating-name-' + index + '-edit"]'; }

  repeatingNameQuestion(index = 0) { return '#repeating-name-question-' + index; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  whoIsRelatedNoPrimary(index = 0) { return '#who-is-related-no-primary-' + index + '-answer'; }

  whoIsRelatedNoPrimaryEdit(index = 0) { return '[data-qa="who-is-related-no-primary-' + index + '-edit"]'; }

  relationshipNoPrimaryQuestion(index = 0) { return '#relationship-no-primary-question-' + index; }

  householdRelationshipsNoPrimaryTitle(index = 0) { return '#household-relationships-no-primary-' + index; }

  whoIsRelated(index = 0) { return '#who-is-related-' + index + '-answer'; }

  whoIsRelatedEdit(index = 0) { return '[data-qa="who-is-related-' + index + '-edit"]'; }

  relationshipQuestion(index = 0) { return '#relationship-question-' + index; }

  householdRelationshipsTitle(index = 0) { return '#household-relationships-' + index; }

  sexAnswerNoPrimary(index = 0) { return '#sex-answer-no-primary-' + index + '-answer'; }

  sexAnswerNoPrimaryEdit(index = 0) { return '[data-qa="sex-answer-no-primary-' + index + '-edit"]'; }

  sexQuestionNoPrimary(index = 0) { return '#sex-question-no-primary-' + index; }

  sexGroupNoPrimaryTitle(index = 0) { return '#sex-group-no-primary-' + index; }

  sexAnswer(index = 0) { return '#sex-answer-' + index + '-answer'; }

  sexAnswerEdit(index = 0) { return '[data-qa="sex-answer-' + index + '-edit"]'; }

  sexQuestion(index = 0) { return '#sex-question-' + index; }

  sexGroupTitle(index = 0) { return '#sex-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
