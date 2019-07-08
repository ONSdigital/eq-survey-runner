const BasePage = require('./base.page');

class HubPage extends BasePage {

  constructor(pageName) {
    super(pageName);
  }

  url() { return "/questionnaire/sections/"; }

  myAccountLink() { return '#my-account'; }

  alert() { return '[data-qa="error-body"]';  }

  error() { return '.js-inpagelink'; }

  errorHeader() { return '#main-content > div.panel.panel--error.u-mb-s > div.panel__header > div'; }

  errorNumber(number = 1) { return '[data-qa="error-body"] ul > li:nth-child(' + number + ') > a'; }

  previous() { return 'a[id="top-previous"]'; }

  displayedName() { return 'h1'; }

  displayedDescription() { return 'p > strong'; }

  submit() { return '[data-qa="btn-submit"]'; }

  saveSignOut() { return '[data-qa="btn-save-sign-out"]'; }

  switchLanguage(language_code) { return 'a[href="?language_code=' + language_code + '"]'; }

  summaryRowState(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__values';
  }

  summaryRowLink(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__actions a';
  }

  summaryRowTitle(number = 1) {
    return 'tbody:nth-child(' + number + ') tr td.summary__item-title';
  }
}

module.exports = new HubPage();
