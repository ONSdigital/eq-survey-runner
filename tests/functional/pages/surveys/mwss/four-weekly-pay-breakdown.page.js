// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FourWeeklyPayBreakdownPage extends QuestionPage {

  constructor() {
    super('four-weekly-pay-breakdown')
  }

  setFourWeeklyPayBreakdownArrearsAnswer(value) {
    browser.setValue('[name="four-weekly-pay-breakdown-arrears-answer"]', value)
    return this
  }

  getFourWeeklyPayBreakdownArrearsAnswer(value) {
    return browser.element('[name="four-weekly-pay-breakdown-arrears-answer"]').getValue()
  }

  setFourWeeklyPayBreakdownPrpAnswer(value) {
    browser.setValue('[name="four-weekly-pay-breakdown-prp-answer"]', value)
    return this
  }

  getFourWeeklyPayBreakdownPrpAnswer(value) {
    return browser.element('[name="four-weekly-pay-breakdown-prp-answer"]').getValue()
  }

}

export default new FourWeeklyPayBreakdownPage()
