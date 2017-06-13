class ConfirmationPage {
  isOpen() {
    const url = browser.url().value
    return url.indexOf('confirmation') > -1
  }

  getSubtitle() {
    return browser.element('[data-qa="section-title"]').getText()
  }

  submit() {
    browser.click('[data-qa="btn-submit"]')
  }

  changeAnswers() {
    browser.click('a[id="top-previous"]')
  }
}

export default new ConfirmationPage()
