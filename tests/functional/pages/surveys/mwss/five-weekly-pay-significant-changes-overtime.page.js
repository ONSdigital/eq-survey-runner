// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesOvertimePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-overtime')
  }

  clickFiveWeeklyPaySignificantChangesOvertimeAnswerMoreOvertime() {
    browser.element('[id="five-weekly-pay-significant-changes-overtime-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesOvertimeAnswerLessOvertime() {
    browser.element('[id="five-weekly-pay-significant-changes-overtime-answer-1"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesOvertimeAnswerNoSignificantChange() {
    browser.element('[id="five-weekly-pay-significant-changes-overtime-answer-2"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesOvertimePage()
