// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FortnightlyPaySignificantChangesRedundanciesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('fortnightly-pay-significant-changes-redundancies')
  }

  clickFortnightlyPaySignificantChangesRedundanciesAnswerYes() {
    browser.element('[id="fortnightly-pay-significant-changes-redundancies-answer-0"]').click()
    return this
  }

  clickFortnightlyPaySignificantChangesRedundanciesAnswerNo() {
    browser.element('[id="fortnightly-pay-significant-changes-redundancies-answer-1"]').click()
    return this
  }

}

export default new FortnightlyPaySignificantChangesRedundanciesPage()
