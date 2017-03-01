// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class CalendarMonthlyPayBreakdownPage extends QuestionPage {

  constructor() {
    super('calendar-monthly-pay-breakdown')
  }

  setCalendarMonthlyPayBreakdownArrearsAnswer(value) {
    browser.setValue('[name="calendar-monthly-pay-breakdown-arrears-answer"]', value)
    return this
  }

  getCalendarMonthlyPayBreakdownArrearsAnswer(value) {
    return browser.element('[name="calendar-monthly-pay-breakdown-arrears-answer"]').getValue()
  }

  setCalendarMonthlyPayBreakdownPrpAnswer(value) {
    browser.setValue('[name="calendar-monthly-pay-breakdown-prp-answer"]', value)
    return this
  }

  getCalendarMonthlyPayBreakdownPrpAnswer(value) {
    return browser.element('[name="calendar-monthly-pay-breakdown-prp-answer"]').getValue()
  }

}

export default new CalendarMonthlyPayBreakdownPage()
