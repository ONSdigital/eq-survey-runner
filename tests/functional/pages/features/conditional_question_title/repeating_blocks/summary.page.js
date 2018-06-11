// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  behalfOfAnswer() { return '#behalf-of-answer-answer'; }

  behalfOfAnswerEdit() { return '[data-qa="behalf-of-answer-edit"]'; }

  firstName() { return '#first-name-answer'; }

  firstNameEdit() { return '[data-qa="first-name-edit"]'; }

  groupTitle() { return '#group'; }

  ageDifference() { return '#age-difference-answer'; }

  ageDifferenceEdit() { return '[data-qa="age-difference-edit"]'; }

  confirmAnswer() { return '#confirm-answer-answer'; }

  confirmAnswerEdit() { return '[data-qa="confirm-answer-edit"]'; }

  repeatingGroupTitle() { return '#repeating-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
