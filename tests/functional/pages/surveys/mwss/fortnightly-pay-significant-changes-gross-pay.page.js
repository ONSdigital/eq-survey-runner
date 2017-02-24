// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesGrossPayPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-gross-pay')
  }

  clickFortnightlyPaySignificantChangesGrossPayAnswerYes() {
    browser.element('[id="fortnightly-pay-significant-changes-gross-pay-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesGrossPayAnswerNo() {
    browser.element('[id="fortnightly-pay-significant-changes-gross-pay-answer-1"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesGrossPayPage()
