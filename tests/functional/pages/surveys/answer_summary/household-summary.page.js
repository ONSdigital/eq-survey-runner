// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class HouseholdSummaryPage extends QuestionPage {

  constructor() {
    super('household-summary');
  }

  primaryFirstNameEdit(index = 1) { return '[data-qa="primary-first-name-' + index + '-edit"]'; }

  primaryFirstNameLabel(index = 1) { return '[data-qa="primary-first-name-' + index + '-label"]'; }

  repeatingFirstNameEdit(index = 1) { return '[data-qa="repeating-first-name-' + index + '-edit"]'; }

  repeatingFirstNameLabel(index = 1) { return '[data-qa="repeating-first-name-' + index + '-label"]'; }

  addPersonLink() { return '#add-person-link'; }

}
module.exports = new HouseholdSummaryPage();
