// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  coffeeAnswer() { return '#coffee-answer-answer'; }

  coffeeAnswerEdit() { return '[data-qa="coffee-answer-edit"]'; }

  responseYesNumberOfCups() { return '#response-yes-number-of-cups-answer'; }

  responseYesNumberOfCupsEdit() { return '[data-qa="response-yes-number-of-cups-edit"]'; }

  responseNoNumberOfCups() { return '#response-no-number-of-cups-answer'; }

  responseNoNumberOfCupsEdit() { return '[data-qa="response-no-number-of-cups-edit"]'; }

  toastAnswer() { return '#toast-answer-answer'; }

  toastAnswerEdit() { return '[data-qa="toast-answer-edit"]'; }

}
module.exports = new SummaryPage();
