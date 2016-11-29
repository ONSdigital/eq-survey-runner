class QuestionPage {

  getAlertText(year) {
    return browser.element('.alert__body').getText()
  }

  submit() {
    browser.click('.qa-btn-submit')
    return this
  }

  errorExists(){
    return browser.isExisting('.js-inpagelink')
  }

  previous(){
    return browser.click('a[id="top-previous"]')
  }

}

export default QuestionPage
