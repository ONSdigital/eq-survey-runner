class BasePage {

  constructor(pageName) {
    this.pageName = pageName;
  }

  isOpen() {
    return browser.getUrl().should.eventually.contain(this.pageName);
  }

}

module.exports = BasePage;
