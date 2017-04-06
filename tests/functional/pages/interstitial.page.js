class InterstitialPage {

  getMainHeading() {
    return browser.element('h1').getText()
  }

  submit() {
    browser.click('[data-qa="btn-submit"]')
  }

}

export default InterstitialPage
