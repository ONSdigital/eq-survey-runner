// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class HouseholdGoodsSalesPage extends QuestionPage {
  constructor() {
    super('household-goods-sales')
  }
  setTotalSalesHouseholdGoods(value) {
    browser.setValue('[name="total-sales-household-goods"]', value)
    return this
  }
  getTotalSalesHouseholdGoods(value) {
    return browser.element('[name="total-sales-household-goods"]').getValue()
  }
  getTotalSalesHouseholdGoodsLabel() {
    return browser.element('#label-total-sales-household-goods')
  }
  getTotalSalesHouseholdGoodsElement() {
    return browser.element('[name="total-sales-household-goods"]')
  }
}

export default new HouseholdGoodsSalesPage()
