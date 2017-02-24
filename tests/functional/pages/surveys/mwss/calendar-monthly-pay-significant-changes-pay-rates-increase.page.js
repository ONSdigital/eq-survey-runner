// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class CalendarMonthlyPaySignificantChangesPayRatesIncreasePage extends QuestionPage {

  constructor() {
    super('calendar-monthly-pay-significant-changes-pay-rates-increase')
  }

  setCalendarMonthlyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    browser.setValue('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]', value)
    return this
  }

  getCalendarMonthlyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    return browser.element('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]').getValue()
  }

  setCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    browser.setValue('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]', value)
    return this
  }

  getCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    return browser.element('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]').getValue()
  }

  setCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    browser.selectByValue('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]', value)
    return this
  }

  getCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    return browser.element('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]').getValue()
  }

  setCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    browser.setValue('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]', value)
    return this
  }

  getCalendarMonthlyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    return browser.element('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]').getValue()
  }

  setCalendarMonthlyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    browser.setValue('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]', value)
    return this
  }

  getCalendarMonthlyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    return browser.element('[name="calendar-monthly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]').getValue()
  }

}

export default new CalendarMonthlyPaySignificantChangesPayRatesIncreasePage()
