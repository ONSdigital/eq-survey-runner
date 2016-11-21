class ThankYou {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('thank-you') > -1
  }

  getMainHeading() {
    return browser.element('h1').getText()
  }

}

export default new ThankYou()
