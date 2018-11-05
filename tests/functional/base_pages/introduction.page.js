const BasePage = require('./base.page');

class IntroductionPage extends BasePage {

  constructor() {
    super('introduction-page');
  }

  myAccountLink() {
    return '#my-account';
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
    return '[data-qa="intro-basic-description"]';
  }

  introTitleDescription() {
    return '[data-qa="details-changed-title"]';
  }
}

module.exports = new IntroductionPage();
