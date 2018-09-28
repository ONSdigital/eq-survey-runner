// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  coffeeAnswer(index = 0) { return '#coffee-answer-' + index + '-answer'; }

  coffeeAnswerEdit(index = 0) { return '[data-qa="coffee-answer-' + index + '-edit"]'; }

  responseYesNumberOfCups(index = 0) { return '#response-yes-number-of-cups-' + index + '-answer'; }

  responseYesNumberOfCupsEdit(index = 0) { return '[data-qa="response-yes-number-of-cups-' + index + '-edit"]'; }

  responseNoNumberOfCups(index = 0) { return '#response-no-number-of-cups-' + index + '-answer'; }

  responseNoNumberOfCupsEdit(index = 0) { return '[data-qa="response-no-number-of-cups-' + index + '-edit"]'; }

  toastAnswer(index = 0) { return '#toast-answer-' + index + '-answer'; }

  toastAnswerEdit(index = 0) { return '[data-qa="toast-answer-' + index + '-edit"]'; }

}
module.exports = new SummaryPage();
