// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class AmountAcquisitionAdvancedMachineryPage extends QuestionPage {

  constructor() {
    super('amount-acquisition-advanced-machinery')
  }

  setAmountAcquisitionAdvancedMachineryAnswer(value) {
    browser.setValue('[name="amount-acquisition-advanced-machinery-answer"]', value)
    return this
  }

  getAmountAcquisitionAdvancedMachineryAnswer(value) {
    return browser.element('[name="amount-acquisition-advanced-machinery-answer"]').getValue()
  }

}

export default new AmountAcquisitionAdvancedMachineryPage()
