const BasePage = require('./base.page');

class QuestionPage extends BasePage {

  constructor(pageName) {
    super(pageName);
    this.questions = [];
  }

  url() { return "/questionnaire/" + this.pageName; }

  myAccountLink() { return '#my-account'; }

  summaryQuestionText() { return '.summary__item-title'; }

  questionText() { return 'h1'; }

  alert() { return '[data-qa="error-body"]';  }

  error() { return '.js-inpagelink'; }

  errorHeader() { return '#main-content > div.panel.panel--error.u-mb-s > div.panel__header > div'; }

  errorNumber(number = 1) { return '[data-qa="error-body"] ul > li:nth-child(' + number + ') > a'; }

  previous() { return 'a[id="top-previous"]'; }

  displayedName() { return '[data-qa="block-title"]'; }

  displayedDescription() { return '[data-qa="block-description"]'; }

  submit() { return '[data-qa="btn-submit"]'; }

  saveSignOut() { return '[data-qa="btn-save-sign-out"]'; }

  interstitialHeader() { return 'main > h1';}

  switchLanguage(language_code) { return 'a[href="?language_code=' + language_code + '"]'; }

}

module.exports = QuestionPage;
