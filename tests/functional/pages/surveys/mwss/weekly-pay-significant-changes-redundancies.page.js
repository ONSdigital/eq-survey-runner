// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesRedundanciesPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-redundancies')
  }

  clickWeeklyPaySignificantChangesRedundanciesAnswerYes() {
    browser.element('[id="weekly-pay-significant-changes-redundancies-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesRedundanciesAnswerNo() {
    browser.element('[id="weekly-pay-significant-changes-redundancies-answer-1"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesRedundanciesPage()
