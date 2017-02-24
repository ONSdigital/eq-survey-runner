// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesOvertimePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-overtime')
  }

  clickFourWeeklyPaySignificantChangesOvertimeAnswerMoreOvertime() {
    browser.element('[id="four-weekly-pay-significant-changes-overtime-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesOvertimeAnswerLessOvertime() {
    browser.element('[id="four-weekly-pay-significant-changes-overtime-answer-1"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesOvertimeAnswerNoSignificantChange() {
    browser.element('[id="four-weekly-pay-significant-changes-overtime-answer-2"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesOvertimePage()
