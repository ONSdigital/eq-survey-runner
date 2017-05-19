const BasePage = require('./base.page');

class LandingPage extends BasePage {

  constructor() {
    super('landing-page');
  }

  getStarted() {
    return '.qa-btn-get-started';
  }

}

exports = new LandingPage();
