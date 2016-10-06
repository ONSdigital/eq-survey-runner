class SummaryPage {

  isOpen() {
    const url = browser.url().value
    return url.indexOf('summary') > -1
  }
  static editLinkChangeEmpFig(){
    browser.click('[aria-describedby="summary-3-0 summary-3-0-answer"]')
  }
  static submit() {
    browser.click('.qa-btn-submit-answers')
  }

}

export default SummaryPage
