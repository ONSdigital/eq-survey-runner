// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesIndustrialActionPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-industrial-action')
  }

  clickFiveWeeklyPaySignificantChangesIndustrialActionAnswerYes() {
    browser.element('[id="five-weekly-pay-significant-changes-industrial-action-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesIndustrialActionAnswerNo() {
    browser.element('[id="five-weekly-pay-significant-changes-industrial-action-answer-1"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesIndustrialActionPage()
