// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FortnightlyPayBreakdownPage extends QuestionPage {

  constructor() {
    super('fortnightly-pay-breakdown')
  }

  setFortnightlyPayBreakdownHolidayAnswer(value) {
    browser.setValue('[name="fortnightly-pay-breakdown-holiday-answer"]', value)
    return this
  }

  getFortnightlyPayBreakdownHolidayAnswer(value) {
    return browser.element('[name="fortnightly-pay-breakdown-holiday-answer"]').getValue()
  }

  setFortnightlyPayBreakdownArrearsAnswer(value) {
    browser.setValue('[name="fortnightly-pay-breakdown-arrears-answer"]', value)
    return this
  }

  getFortnightlyPayBreakdownArrearsAnswer(value) {
    return browser.element('[name="fortnightly-pay-breakdown-arrears-answer"]').getValue()
  }

  setFortnightlyPayBreakdownPrpAnswer(value) {
    browser.setValue('[name="fortnightly-pay-breakdown-prp-answer"]', value)
    return this
  }

  getFortnightlyPayBreakdownPrpAnswer(value) {
    return browser.element('[name="fortnightly-pay-breakdown-prp-answer"]').getValue()
  }

}

export default new FortnightlyPayBreakdownPage()
