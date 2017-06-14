// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class OtherGoodsSalesPage extends QuestionPage {
  constructor() {
    super('other-goods-sales')
  }
  setTotalSalesOtherGoods(value) {
    browser.setValue('[name="total-sales-other-goods"]', value)
    return this
  }
  getTotalSalesOtherGoods(value) {
    return browser.element('[name="total-sales-other-goods"]').getValue()
  }
  getTotalSalesOtherGoodsLabel() {
    return browser.element('#label-total-sales-other-goods')
  }
  getTotalSalesOtherGoodsElement() {
    return browser.element('[name="total-sales-other-goods"]')
  }
}

export default new OtherGoodsSalesPage()
