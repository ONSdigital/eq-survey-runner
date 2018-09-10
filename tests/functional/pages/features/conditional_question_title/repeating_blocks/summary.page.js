// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../../surveys/question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  behalfOfAnswer(index = 0) { return '#behalf-of-answer-' + index + '-answer'; }

  behalfOfAnswerEdit(index = 0) { return '[data-qa="behalf-of-answer-' + index + '-edit"]'; }

  firstName(index = 0) { return '#first-name-' + index + '-answer'; }

  firstNameEdit(index = 0) { return '[data-qa="first-name-' + index + '-edit"]'; }

  groupTitle(index = 0) { return '#group-' + index; }

  ageDifference(index = 0) { return '#age-difference-' + index + '-answer'; }

  ageDifferenceEdit(index = 0) { return '[data-qa="age-difference-' + index + '-edit"]'; }

  confirmAnswer(index = 0) { return '#confirm-answer-' + index + '-answer'; }

  confirmAnswerEdit(index = 0) { return '[data-qa="confirm-answer-' + index + '-edit"]'; }

  repeatingGroupTitle(index = 0) { return '#repeating-group-' + index; }

  summaryGroupTitle(index = 0) { return '#summary-group-' + index; }

}
module.exports = new SummaryPage();
