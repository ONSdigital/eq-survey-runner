class SummaryPage {

  static isOpen() {
    const url = browser.url().value
    return url.indexOf('summary') > -1
  }

  static submit() {
    browser.click('[data-qa="btn-submit"]')
  }

}

export default SummaryPage
