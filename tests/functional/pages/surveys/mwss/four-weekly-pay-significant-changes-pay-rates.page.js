// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesPayRatesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-pay-rates')
  }

  clickFourWeeklyPaySignificantChangesPayRatesAnswerYes() {
    browser.element('[id="four-weekly-pay-significant-changes-pay-rates-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesPayRatesAnswerNo() {
    browser.element('[id="four-weekly-pay-significant-changes-pay-rates-answer-1"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesPayRatesPage()
