class QuestionPage {

  getAlertText(year) {
    return browser.element('.alert__body').getText()
  }

  submit() {
    browser.click('.qa-btn-submit')
    return this
  }

}

export default QuestionPage
