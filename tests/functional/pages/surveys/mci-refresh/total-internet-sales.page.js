// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class TotalInternetSalesPage extends QuestionPage {
  constructor() {
    super('total-internet-sales')
  }
  setInternetSales(value) {
    browser.setValue('[name="internet-sales"]', value)
    return this
  }
  getInternetSales(value) {
    return browser.element('[name="internet-sales"]').getValue()
  }
  getInternetSalesLabel() {
    return browser.element('#label-internet-sales')
  }
  getInternetSalesElement() {
    return browser.element('[name="internet-sales"]')
  }
}

export default new TotalInternetSalesPage()
