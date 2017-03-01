// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class WeeklyPaySignificantChangesGrossPayPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('weekly-pay-significant-changes-gross-pay')
  }

  clickWeeklyPaySignificantChangesGrossPayAnswerYes() {
    browser.element('[id="weekly-pay-significant-changes-gross-pay-answer-0"]').click()
    return this
  }

  clickWeeklyPaySignificantChangesGrossPayAnswerNo() {
    browser.element('[id="weekly-pay-significant-changes-gross-pay-answer-1"]').click()
    return this
  }

}

export default new WeeklyPaySignificantChangesGrossPayPage()
