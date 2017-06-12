// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ClothingSalesPage extends QuestionPage {
  constructor() {
    super('clothing-sales')
  }
  setTotalSalesClothing(value) {
    browser.setValue('[name="total-sales-clothing"]', value)
    return this
  }
  getTotalSalesClothing(value) {
    return browser.element('[name="total-sales-clothing"]').getValue()
  }
  getTotalSalesClothingLabel() {
    return browser.element('#label-total-sales-clothing')
  }
  getTotalSalesClothingElement() {
    return browser.element('[name="total-sales-clothing"]')
  }
}

export default new ClothingSalesPage()
