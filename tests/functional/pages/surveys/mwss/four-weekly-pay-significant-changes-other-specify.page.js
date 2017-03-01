// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FourWeeklyPaySignificantChangesOtherSpecifyPage extends QuestionPage {

  constructor() {
    super('four-weekly-pay-significant-changes-other-specify')
  }

  setFourWeeklyPaySignificantChangesOtherSpecifyAnswer(value) {
    browser.setValue('[name="four-weekly-pay-significant-changes-other-specify-answer"]', value)
    return this
  }

  getFourWeeklyPaySignificantChangesOtherSpecifyAnswer(value) {
    return browser.element('[name="four-weekly-pay-significant-changes-other-specify-answer"]').getValue()
  }

}

export default new FourWeeklyPaySignificantChangesOtherSpecifyPage()
