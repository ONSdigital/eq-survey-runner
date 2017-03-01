// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesPayRatesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-pay-rates')
  }

  clickFortnightlyPaySignificantChangesPayRatesAnswerYes() {
    browser.element('[id="fortnightly-pay-significant-changes-pay-rates-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesPayRatesAnswerNo() {
    browser.element('[id="fortnightly-pay-significant-changes-pay-rates-answer-1"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesPayRatesPage()
