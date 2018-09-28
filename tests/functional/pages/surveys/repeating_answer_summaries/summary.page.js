// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  primaryLastName(index = 0) { return '#primary-last-name-' + index + '-answer'; }

  primaryLastNameEdit(index = 0) { return '[data-qa="primary-last-name-' + index + '-edit"]'; }

  primaryAnyoneElse(index = 0) { return '#primary-anyone-else-' + index + '-answer'; }

  primaryAnyoneElseEdit(index = 0) { return '[data-qa="primary-anyone-else-' + index + '-edit"]'; }

  primaryGroupTitle(index = 0) { return '#primary-group-' + index; }

  repeatingLastName(index = 0) { return '#repeating-last-name-' + index + '-answer'; }

  repeatingLastNameEdit(index = 0) { return '[data-qa="repeating-last-name-' + index + '-edit"]'; }

  repeatingAnyoneElse(index = 0) { return '#repeating-anyone-else-' + index + '-answer'; }

  repeatingAnyoneElseEdit(index = 0) { return '[data-qa="repeating-anyone-else-' + index + '-edit"]'; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
