class LandingPage {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('introduction') > -1
  }

  getStarted() {
    browser.click('.qa-btn-get-started')
    return this
  }

}

export default new LandingPage()
