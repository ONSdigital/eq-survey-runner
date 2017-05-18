// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class TotalRetailTurnoverBlockPage extends QuestionPage {
  constructor() {
    super('total-retail-turnover-block')
  }
  setTotalRetailTurnover(value) {
    browser.setValue('[name="total-retail-turnover"]', value)
    return this
  }
  getTotalRetailTurnover(value) {
    return browser.element('[name="total-retail-turnover"]').getValue()
  }
  getTotalRetailTurnoverLabel() {
    return browser.element('#label-total-retail-turnover')
  }
  getTotalRetailTurnoverElement() {
    return browser.element('[name="total-retail-turnover"]')
  }
}

export default new TotalRetailTurnoverBlockPage()
