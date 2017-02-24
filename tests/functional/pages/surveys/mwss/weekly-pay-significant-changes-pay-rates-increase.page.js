// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class WeeklyPaySignificantChangesPayRatesIncreasePage extends QuestionPage {

  constructor() {
    super('weekly-pay-significant-changes-pay-rates-increase')
  }

  setWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    browser.setValue('[name="weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]', value)
    return this
  }

  getWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    return browser.element('[name="weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]').getValue()
  }

  setWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    browser.setValue('[name="weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]', value)
    return this
  }

  getWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    return browser.element('[name="weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]').getValue()
  }

  setWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    browser.selectByValue('[name="weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]', value)
    return this
  }

  getWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    return browser.element('[name="weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]').getValue()
  }

  setWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    browser.setValue('[name="weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]', value)
    return this
  }

  getWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    return browser.element('[name="weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]').getValue()
  }

  setWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    browser.setValue('[name="weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]', value)
    return this
  }

  getWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    return browser.element('[name="weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]').getValue()
  }

}

export default new WeeklyPaySignificantChangesPayRatesIncreasePage()
