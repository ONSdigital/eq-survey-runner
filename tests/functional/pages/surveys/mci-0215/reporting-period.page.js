// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ReportingPeriodPage extends QuestionPage {
  constructor() {
    super('reporting-period')
  }
  setPeriodFromDay(value) {
    browser.setValue('[name="period-from-day"]', value)
    return this
  }
  getPeriodFromDay(value) {
    return browser.element('[name="period-from-day"]').getValue()
  }
  setPeriodFromMonth(value) {
    browser.selectByValue('[name="period-from-month"]', value)
    return this
  }
  getPeriodFromMonth(value) {
    return browser.element('[name="period-from-month"]').getValue()
  }
  setPeriodFromYear(value) {
    browser.setValue('[name="period-from-year"]', value)
    return this
  }
  getPeriodFromYear(value) {
    return browser.element('[name="period-from-year"]').getValue()
  }
  setPeriodToDay(value) {
    browser.setValue('[name="period-to-day"]', value)
    return this
  }
  getPeriodToDay(value) {
    return browser.element('[name="period-to-day"]').getValue()
  }
  setPeriodToMonth(value) {
    browser.selectByValue('[name="period-to-month"]', value)
    return this
  }
  getPeriodToMonth(value) {
    return browser.element('[name="period-to-month"]').getValue()
  }
  setPeriodToYear(value) {
    browser.setValue('[name="period-to-year"]', value)
    return this
  }
  getPeriodToYear(value) {
    return browser.element('[name="period-to-year"]').getValue()
  }
}

export default new ReportingPeriodPage()
