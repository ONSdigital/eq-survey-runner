class SummaryPage {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('summary') > -1
  }

  submit() {
    browser.click('.qa-btn-submit-answers')
    return this
  }

}

export default new SummaryPage()
