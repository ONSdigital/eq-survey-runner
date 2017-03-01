// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../multiple-choice.page'

class FiveWeeklyPaySignificantChangesOtherPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('five-weekly-pay-significant-changes-other')
  }

  clickFiveWeeklyPaySignificantChangesOtherAnswerYes() {
    browser.element('[id="five-weekly-pay-significant-changes-other-answer-0"]').click()
    return this
  }

  clickFiveWeeklyPaySignificantChangesOtherAnswerNo() {
    browser.element('[id="five-weekly-pay-significant-changes-other-answer-1"]').click()
    return this
  }

}

export default new FiveWeeklyPaySignificantChangesOtherPage()
