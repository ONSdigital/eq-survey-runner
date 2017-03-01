// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesOtherPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-other')
  }

  clickFortnightlyPaySignificantChangesOtherAnswerYes() {
    browser.element('[id="fortnightly-pay-significant-changes-other-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesOtherAnswerNo() {
    browser.element('[id="fortnightly-pay-significant-changes-other-answer-1"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesOtherPage()
