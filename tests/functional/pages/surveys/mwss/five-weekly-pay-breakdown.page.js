// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FiveWeeklyPayBreakdownPage extends QuestionPage {

  constructor() {
    super('five-weekly-pay-breakdown')
  }

  setFiveWeeklyPayBreakdownArrearsAnswer(value) {
    browser.setValue('[name="five-weekly-pay-breakdown-arrears-answer"]', value)
    return this
  }

  getFiveWeeklyPayBreakdownArrearsAnswer(value) {
    return browser.element('[name="five-weekly-pay-breakdown-arrears-answer"]').getValue()
  }

  setFiveWeeklyPayBreakdownPrpAnswer(value) {
    browser.setValue('[name="five-weekly-pay-breakdown-prp-answer"]', value)
    return this
  }

  getFiveWeeklyPayBreakdownPrpAnswer(value) {
    return browser.element('[name="five-weekly-pay-breakdown-prp-answer"]').getValue()
  }

}

export default new FiveWeeklyPayBreakdownPage()
