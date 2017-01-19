// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class AmountAcquisitionInternalInvestmentRDPage extends QuestionPage {

  constructor() {
    super('amount-acquisition-internal-investment-r-d')
  }

  setAmountAcquisitionInternalInvestmentRDAnswer(value) {
    browser.setValue('[name="amount-acquisition-internal-investment-r-d-answer"]', value)
    return this
  }

  getAmountAcquisitionInternalInvestmentRDAnswer(value) {
    return browser.element('[name="amount-acquisition-internal-investment-r-d-answer"]').getValue()
  }

}

export default new AmountAcquisitionInternalInvestmentRDPage()
