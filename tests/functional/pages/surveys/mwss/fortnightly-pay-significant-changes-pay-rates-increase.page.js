// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FortnightlyPaySignificantChangesPayRatesIncreasePage extends QuestionPage {

  constructor() {
    super('fortnightly-pay-significant-changes-pay-rates-increase')
  }

  setFortnightlyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    browser.setValue('[name="fortnightly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]', value)
    return this
  }

  getFortnightlyPaySignificantChangesPayRatesIncreasePercentIncreaseAnswer(value) {
    return browser.element('[name="fortnightly-pay-significant-changes-pay-rates-increase-percent-increase-answer"]').getValue()
  }

  setFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    browser.setValue('[name="fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]', value)
    return this
  }

  getFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerDay(value) {
    return browser.element('[name="fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-day"]').getValue()
  }

  setFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    browser.selectByValue('[name="fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]', value)
    return this
  }

  getFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerMonth(value) {
    return browser.element('[name="fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-month"]').getValue()
  }

  setFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    browser.setValue('[name="fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]', value)
    return this
  }

  getFortnightlyPaySignificantChangesPayRatesIncreaseDateFromAnswerYear(value) {
    return browser.element('[name="fortnightly-pay-significant-changes-pay-rates-increase-date-from-answer-year"]').getValue()
  }

  setFortnightlyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    browser.setValue('[name="fortnightly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]', value)
    return this
  }

  getFortnightlyPaySignificantChangesPayRatesIncreasePercentEmployeesAnswer(value) {
    return browser.element('[name="fortnightly-pay-significant-changes-pay-rates-increase-percent-employees-answer"]').getValue()
  }

}

export default new FortnightlyPaySignificantChangesPayRatesIncreasePage()
