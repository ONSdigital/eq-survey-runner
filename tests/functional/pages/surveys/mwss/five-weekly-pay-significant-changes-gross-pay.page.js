// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesGrossPayPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-gross-pay')
  }

  clickFiveWeeklyPaySignificantChangesGrossPayAnswerYes() {
    browser.element('[id="five-weekly-pay-significant-changes-gross-pay-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesGrossPayAnswerNo() {
    browser.element('[id="five-weekly-pay-significant-changes-gross-pay-answer-1"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesGrossPayPage()
