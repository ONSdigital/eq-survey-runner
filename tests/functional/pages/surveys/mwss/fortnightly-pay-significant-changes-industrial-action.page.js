// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesIndustrialActionPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-industrial-action')
  }

  clickFortnightlyPaySignificantChangesIndustrialActionAnswerYes() {
    browser.element('[id="fortnightly-pay-significant-changes-industrial-action-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesIndustrialActionAnswerNo() {
    browser.element('[id="fortnightly-pay-significant-changes-industrial-action-answer-1"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesIndustrialActionPage()
