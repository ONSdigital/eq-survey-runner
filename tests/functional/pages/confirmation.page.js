class ConfirmationPage {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('confirmation') > -1
  }

  getSubtitle() {
    return browser.element('h2').getText()
  }

  submit() {
    browser.click('.qa-btn-submit-answers')
  }

  changeAnswers() {
    return browser.click('a[id="top-previous"]')
  }

}

export default new ConfirmationPage()
