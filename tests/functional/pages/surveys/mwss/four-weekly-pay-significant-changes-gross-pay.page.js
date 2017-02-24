// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FourWeeklyPaySignificantChangesGrossPayPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('four-weekly-pay-significant-changes-gross-pay')
  }

  clickFourWeeklyPaySignificantChangesGrossPayAnswerYes() {
    browser.element('[id="four-weekly-pay-significant-changes-gross-pay-answer-0"]').click()
    return this
  }

  clickFourWeeklyPaySignificantChangesGrossPayAnswerNo() {
    browser.element('[id="four-weekly-pay-significant-changes-gross-pay-answer-1"]').click()
    return this
  }

}

export default new FourWeeklyPaySignificantChangesGrossPayPage()
