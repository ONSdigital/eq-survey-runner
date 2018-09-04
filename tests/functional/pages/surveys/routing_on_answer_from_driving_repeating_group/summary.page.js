// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  primaryName() { return '#primary-name-answer'; }

  primaryNameEdit() { return '[data-qa="primary-name-edit"]'; }

  primaryLiveHere() { return '#primary-live-here-answer'; }

  primaryLiveHereEdit() { return '[data-qa="primary-live-here-edit"]'; }

  primaryGroupTitle() { return '#primary-group'; }

  repeatingAnyoneElse() { return '#repeating-anyone-else-answer'; }

  repeatingAnyoneElseEdit() { return '[data-qa="repeating-anyone-else-edit"]'; }

  repeatingName() { return '#repeating-name-answer'; }

  repeatingNameEdit() { return '[data-qa="repeating-name-edit"]'; }

  repeatingGroupTitle() { return '#repeating-group'; }

  whoIsRelated() { return '#who-is-related-answer'; }

  whoIsRelatedEdit() { return '[data-qa="who-is-related-edit"]'; }

  householdRelationshipsTitle() { return '#household-relationships'; }

  sexAnswer() { return '#sex-answer-answer'; }

  sexAnswerEdit() { return '[data-qa="sex-answer-edit"]'; }

  sexGroupTitle() { return '#sex-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
