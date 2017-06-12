// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class AlcoholSalesPage extends QuestionPage {
  constructor() {
    super('alcohol-sales')
  }
  setTotalSalesAlcohol(value) {
    browser.setValue('[name="total-sales-alcohol"]', value)
    return this
  }
  getTotalSalesAlcohol(value) {
    return browser.element('[name="total-sales-alcohol"]').getValue()
  }
  getTotalSalesAlcoholLabel() {
    return browser.element('#label-total-sales-alcohol')
  }
  getTotalSalesAlcoholElement() {
    return browser.element('[name="total-sales-alcohol"]')
  }
}

export default new AlcoholSalesPage()
