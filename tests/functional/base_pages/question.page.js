const BasePage = require('./base.page');

class QuestionPage extends BasePage {

  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  myAccountLink() { return '#my-account'; }

  summaryQuestionText() { return '[data-qa="summary-question-title"]'; }

  questionText() { return '[data-qa="question-title"]'; }

  alert() { return '[data-qa="error-body"]';  }

  error() { return '.js-inpagelink'; }

  errorHeader() { return '#main > div.panel.panel--error.u-mb-s > div.panel__header > h1'; }

  errorNumber(number = 1) { return '[data-qa="error-body"] ul > li:nth-child(' + number + ') > a'; }

  previous() { return 'a[id="top-previous"]'; }

  displayedName() { return '[data-qa="block-title"]'; }

  displayedDescription() { return '[data-qa="block-description"]'; }

  submit() { return '[data-qa="btn-submit"]'; }

  saveSignOut() { return '[data-qa="btn-save-sign-out"]'; }

  interstitialHeader() { return '#main > form > h1';}

  switchLanguage(language_code) { return '[data-qa="switch-language-' + language_code + '"]'; }

}

module.exports = QuestionPage;
