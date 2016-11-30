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

  getDisplayedName() {
    return browser.getText('h1[class="section__title saturn"]')
  }

}

export default QuestionPage
