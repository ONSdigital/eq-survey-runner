// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class AutomotiveFuelPage extends QuestionPage {
  constructor() {
    super('automotive-fuel')
  }
  setTotalSalesAutomotiveFuel(value) {
    browser.setValue('[name="total-sales-automotive-fuel"]', value)
    return this
  }
  getTotalSalesAutomotiveFuel(value) {
    return browser.element('[name="total-sales-automotive-fuel"]').getValue()
  }
  getTotalSalesAutomotiveFuelLabel() {
    return browser.element('#label-total-sales-automotive-fuel')
  }
  getTotalSalesAutomotiveFuelElement() {
    return browser.element('[name="total-sales-automotive-fuel"]')
  }
}

export default new AutomotiveFuelPage()
