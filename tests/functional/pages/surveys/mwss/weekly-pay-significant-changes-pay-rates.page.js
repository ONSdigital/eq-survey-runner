// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesPayRatesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-pay-rates')
  }

  clickWeeklyPaySignificantChangesPayRatesAnswerYes() {
    browser.element('[id="weekly-pay-significant-changes-pay-rates-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesPayRatesAnswerNo() {
    browser.element('[id="weekly-pay-significant-changes-pay-rates-answer-1"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesPayRatesPage()
