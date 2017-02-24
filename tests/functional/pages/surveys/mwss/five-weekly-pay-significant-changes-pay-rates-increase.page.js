// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FiveWeeklyPaySignificantChangesPayRatesIncreasePage extends QuestionPage {

  constructor() {
    super('five-weekly-pay-significant-changes-pay-rates-increase')
  }

  setFiveWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    browser.setValue('[name="five-weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]', value)
    return this
  }

  getFiveWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    return browser.element('[name="five-weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]').getValue()
  }

  setFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    browser.setValue('[name="five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]', value)
    return this
  }

  getFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    return browser.element('[name="five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]').getValue()
  }

  setFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    browser.selectByValue('[name="five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]', value)
    return this
  }

  getFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    return browser.element('[name="five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]').getValue()
  }

  setFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    browser.setValue('[name="five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]', value)
    return this
  }

  getFiveWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    return browser.element('[name="five-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]').getValue()
  }

  setFiveWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    browser.setValue('[name="five-weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]', value)
    return this
  }

  getFiveWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    return browser.element('[name="five-weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]').getValue()
  }

}

export default new FiveWeeklyPaySignificantChangesPayRatesIncreasePage()
