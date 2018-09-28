// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  primaryName(index = 0) { return '#primary-name-' + index + 'answer'; }

  primaryNameEdit(index = 0) { return '[data-qa="primary-name-' + index + '-edit"]'; }

  primaryLiveHere(index = 0) { return '#primary-live-here-' + index + '-answer'; }

  primaryLiveHereEdit(index = 0) { return '[data-qa="primary-live-here-' + index + '-edit"]'; }

  primaryGroupTitle(index = 0) { return '#primary-group-' + index; }

  repeatingAnyoneElse(index = 0) { return '#repeating-anyone-else-' + index + '-answer'; }

  repeatingAnyoneElseEdit(index = 0) { return '[data-qa="repeating-anyone-else-' + index + '-edit"]'; }

  repeatingName(index = 0) { return '#repeating-name-' + index + '-answer'; }

  repeatingNameEdit(index = 0) { return '[data-qa="repeating-name-' + index + '-edit"]'; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  whoIsRelated(index = 0) { return '#who-is-related-' + index + '-answer'; }

  whoIsRelatedEdit(index = 0) { return '[data-qa="who-is-related-' + index + '-edit"]'; }

  householdRelationshipsTitle(index = 0) { return '#household-relationships-' + index; }

  sexAnswer(index = 0) { return '#sex-answer-answer-' + index; }

  sexAnswerEdit(index = 0) { return '[data-qa="sex-answer-' + index + '-edit"]'; }

  sexGroupTitle(index = 0) { return '#sex-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
