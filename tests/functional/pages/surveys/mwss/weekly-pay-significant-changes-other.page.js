// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesOtherPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-other')
  }

  clickWeeklyPaySignificantChangesOtherAnswerYes() {
    browser.element('[id="weekly-pay-significant-changes-other-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesOtherAnswerNo() {
    browser.element('[id="weekly-pay-significant-changes-other-answer-1"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesOtherPage()
