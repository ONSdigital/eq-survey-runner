// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  primaryLastName() { return '#primary-last-name-answer'; }

  primaryLastNameEdit() { return '[data-qa="primary-last-name-edit"]'; }

  primaryAnyoneElse() { return '#primary-anyone-else-answer'; }

  primaryAnyoneElseEdit() { return '[data-qa="primary-anyone-else-edit"]'; }

  primaryGroupTitle() { return '#primary-group'; }

  repeatingLastName() { return '#repeating-last-name-answer'; }

  repeatingLastNameEdit() { return '[data-qa="repeating-last-name-edit"]'; }

  repeatingAnyoneElse() { return '#repeating-anyone-else-answer'; }

  repeatingAnyoneElseEdit() { return '[data-qa="repeating-anyone-else-edit"]'; }

  repeatingGroupTitle() { return '#repeating-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
