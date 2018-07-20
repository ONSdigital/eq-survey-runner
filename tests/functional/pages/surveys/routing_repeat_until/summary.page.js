// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  primaryName() { return '#primary-name-answer'; }

  primaryNameEdit() { return '[data-qa="primary-name-edit"]'; }

  primaryAnyoneElse() { return '#primary-anyone-else-answer'; }

  primaryAnyoneElseEdit() { return '[data-qa="primary-anyone-else-edit"]'; }

  primaryGroupTitle() { return '#primary-group'; }

  repeatingName() { return '#repeating-name-answer'; }

  repeatingNameEdit() { return '[data-qa="repeating-name-edit"]'; }

  repeatingAnyoneElse() { return '#repeating-anyone-else-answer'; }

  repeatingAnyoneElseEdit() { return '[data-qa="repeating-anyone-else-edit"]'; }

  repeatingGroupTitle() { return '#repeating-group'; }

  sexAnswer() { return '#sex-answer-answer'; }

  sexAnswerEdit() { return '[data-qa="sex-answer-edit"]'; }

  sexGroupTitle() { return '#sex-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
