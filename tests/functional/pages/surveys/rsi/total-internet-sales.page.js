// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class TotalInternetSalesPage extends QuestionPage {
  constructor() {
    super('total-internet-sales')
  }
  setInternetSales(value) {
    browser.setValue('[name="internet-sales-answer"]', value)
    return this
  }
  getInternetSales(value) {
    return browser.element('[name="internet-sales-answer"]').getValue()
  }
  getInternetSalesLabel() {
    return browser.element('#label-internet-sales-answer')
  }
  getInternetSalesElement() {
    return browser.element('[name="internet-sales-answer"]')
  }
}

export default new TotalInternetSalesPage()
