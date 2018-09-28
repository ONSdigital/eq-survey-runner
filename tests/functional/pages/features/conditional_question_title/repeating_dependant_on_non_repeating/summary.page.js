// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  favColourAnswer(index = 0) { return '#fav-colour-answer-' + index + '-answer'; }

  favColourAnswerEdit(index = 0) { return '[data-qa="fav-colour-answer-' + index + '-edit"]'; }

  colourGroupTitle(index = 0) { return '#colour-group-' + index; }

  firstName(index = 0) { return '#first-name-' + index + '-answer'; }

  firstNameEdit(index = 0) { return '[data-qa="first-name-' + index + '-edit"]'; }

  groupTitle(index = 0) { return '#group-' + index; }

  confirmAnswer(index = 0) { return '#confirm-answer-' + index + '-answer'; }

  confirmAnswerEdit(index = 0) { return '[data-qa="confirm-answer-' + index + '-edit"]'; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
