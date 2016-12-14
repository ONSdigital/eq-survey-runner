class QuestionPage {

  constructor(pageName) {
    this.pageName = pageName
  }

  isOpen() {
    const url = browser.url().value
    return url.indexOf(this.pageName) > -1
  }

  getAlertText() {
    return browser.element('[data-qa="error-body"]').getText()
  }

  submit() {
    if (this.pageName !== undefined) {
        browser.waitUntil(() => this.isOpen(), 500, `Expected to be on ${this.pageName} page but was on ${browser.getUrl()}`)
    }
    browser.click('.qa-btn-submit')
    return this
  }

  errorExists() {
    return browser.isExisting('.js-inpagelink')
  }

  getErrorMsg() {
    return browser.element('.js-inpagelink').getText()
  }

  previous() {
    return browser.click('a[id="top-previous"]')
  }

  getDisplayedName() {
    return browser.getText('h1[class="section__title saturn"]')
  }

}

export default QuestionPage
