// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FoodSalesPage extends QuestionPage {
  constructor() {
    super('food-sales')
  }
  setTotalSalesFood(value) {
    browser.setValue('[name="total-sales-food"]', value)
    return this
  }
  getTotalSalesFood(value) {
    return browser.element('[name="total-sales-food"]').getValue()
  }
  getTotalSalesFoodLabel() {
    return browser.element('#label-total-sales-food')
  }
  getTotalSalesFoodElement() {
    return browser.element('[name="total-sales-food"]')
  }
}

export default new FoodSalesPage()
