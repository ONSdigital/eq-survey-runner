// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesRedundanciesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-redundancies')
  }

  clickFourWeeklyPaySignificantChangesRedundanciesAnswerYes() {
    browser.element('[id="four-weekly-pay-significant-changes-redundancies-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesRedundanciesAnswerNo() {
    browser.element('[id="four-weekly-pay-significant-changes-redundancies-answer-1"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesRedundanciesPage()
