// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class TotalRetailTurnoverBlockPage extends QuestionPage {
  constructor() {
    super('total-retail-turnover-block')
  }
  setTotalRetailTurnover(value) {
    browser.setValue('[name="total-retail-turnover-answer"]', value)
    return this
  }
  getTotalRetailTurnover(value) {
    return browser.element('[name="total-retail-turnover-answer"]').getValue()
  }
  getTotalRetailTurnoverLabel() {
    return browser.element('#label-total-retail-turnover-answer')
  }
  getTotalRetailTurnoverElement() {
    return browser.element('[name="total-retail-turnover-answer"]')
  }
}

export default new TotalRetailTurnoverBlockPage()
