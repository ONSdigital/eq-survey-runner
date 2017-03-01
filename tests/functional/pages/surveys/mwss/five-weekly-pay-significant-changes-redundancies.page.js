// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesRedundanciesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-redundancies')
  }

  clickFiveWeeklyPaySignificantChangesRedundanciesAnswerYes() {
    browser.element('[id="five-weekly-pay-significant-changes-redundancies-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesRedundanciesAnswerNo() {
    browser.element('[id="five-weekly-pay-significant-changes-redundancies-answer-1"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesRedundanciesPage()
