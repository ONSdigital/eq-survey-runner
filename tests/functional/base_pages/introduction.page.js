const BasePage = require('./base.page');

class IntroductionPage extends BasePage {

  constructor(pageName) {
    super(pageName);
  }

  myAccountLink() {
    return '#my-account';
  }

  signOut() {
    return '[data-qa="btn-sign-out"]';
  }

  getStarted() {
    return '.qa-btn-get-started';
  }

  useOfInformation() {
    return '#use-of-information';
  }

  useOfData() {
    return '#how-we-use-your-data';
  }

  legalResponse() {
      return '[data-qa="legal-response"]';
  }

  legalBasis() {
      return '[data-qa="legal-basis"]';
  }

  introDescription() {
    return '#use-of-information p';
  }

  introTitleDescription() {
    return '[data-qa="details-changed-title"]';
  }
}

module.exports = IntroductionPage;
