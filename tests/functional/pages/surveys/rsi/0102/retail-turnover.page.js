import QuestionPage from '../../question.page'

class RetailTurnoverPage extends QuestionPage {

  setRetailTurnover(turnover) {
    browser.setValue('[name="total-retail-turnover-answer"]', turnover)
    return this
  }
  getRetailTurnover() {
    return browser.element('[name="total-retail-turnover-answer"]').getValue()
  }

  saveSignOut() {
    browser.click('button[name="action[save_sign_out]"]')
    return this
  }

  isOpen() {
    const url = browser.url().value
    return url.indexOf('total-retail-turnover') > -1
  }

}

export default new RetailTurnoverPage()
