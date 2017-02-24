// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesPayRatesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-pay-rates')
  }

  clickFiveWeeklyPaySignificantChangesPayRatesAnswerYes() {
    browser.element('[id="five-weekly-pay-significant-changes-pay-rates-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesPayRatesAnswerNo() {
    browser.element('[id="five-weekly-pay-significant-changes-pay-rates-answer-1"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesPayRatesPage()
