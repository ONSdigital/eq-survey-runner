// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FourWeeklyPaySignificantChangesPayRatesIncreasePage extends QuestionPage {

  constructor() {
    super('four-weekly-pay-significant-changes-pay-rates-increase')
  }

  setFourWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    browser.setValue('[name="four-weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]', value)
    return this
  }

  getFourWeeklyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    return browser.element('[name="four-weekly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]').getValue()
  }

  setFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    browser.setValue('[name="four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]', value)
    return this
  }

  getFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    return browser.element('[name="four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]').getValue()
  }

  setFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    browser.selectByValue('[name="four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]', value)
    return this
  }

  getFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    return browser.element('[name="four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]').getValue()
  }

  setFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    browser.setValue('[name="four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]', value)
    return this
  }

  getFourWeeklyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    return browser.element('[name="four-weekly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]').getValue()
  }

  setFourWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    browser.setValue('[name="four-weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]', value)
    return this
  }

  getFourWeeklyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    return browser.element('[name="four-weekly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]').getValue()
  }

}

export default new FourWeeklyPaySignificantChangesPayRatesIncreasePage()
