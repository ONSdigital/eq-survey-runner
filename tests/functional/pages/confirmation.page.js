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
    browser.click('.u-dib')
  }

}

export default new ConfirmationPage()
