// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  favColourAnswer() { return '#fav-colour-answer-answer'; }

  favColourAnswerEdit() { return '[data-qa="fav-colour-answer-edit"]'; }

  colourGroupTitle() { return '#colour-group'; }

  firstName() { return '#first-name-answer'; }

  firstNameEdit() { return '[data-qa="first-name-edit"]'; }

  groupTitle() { return '#group'; }

  confirmAnswer() { return '#confirm-answer-answer'; }

  confirmAnswerEdit() { return '[data-qa="confirm-answer-edit"]'; }

  repeatingGroupTitle() { return '#repeating-group'; }

  summaryGroupTitle() { return '#summary-group'; }

}
module.exports = new SummaryPage();
