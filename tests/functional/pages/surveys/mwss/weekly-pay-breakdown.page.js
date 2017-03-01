// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class WeeklyPayBreakdownPage extends QuestionPage {

  constructor() {
    super('weekly-pay-breakdown')
  }

  setWeeklyPayBreakdownHolidayAnswer(value) {
    browser.setValue('[name="weekly-pay-breakdown-holiday-answer"]', value)
    return this
  }

  getWeeklyPayBreakdownHolidayAnswer(value) {
    return browser.element('[name="weekly-pay-breakdown-holiday-answer"]').getValue()
  }

  setWeeklyPayBreakdownArrearsAnswer(value) {
    browser.setValue('[name="weekly-pay-breakdown-arrears-answer"]', value)
    return this
  }

  getWeeklyPayBreakdownArrearsAnswer(value) {
    return browser.element('[name="weekly-pay-breakdown-arrears-answer"]').getValue()
  }

  setWeeklyPayBreakdownPrpAnswer(value) {
    browser.setValue('[name="weekly-pay-breakdown-prp-answer"]', value)
    return this
  }

  getWeeklyPayBreakdownPrpAnswer(value) {
    return browser.element('[name="weekly-pay-breakdown-prp-answer"]').getValue()
  }

}

export default new WeeklyPayBreakdownPage()
