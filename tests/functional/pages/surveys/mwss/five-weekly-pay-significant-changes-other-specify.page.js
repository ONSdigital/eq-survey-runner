// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FiveWeeklyPaySignificantChangesOtherSpecifyPage extends QuestionPage {

  constructor() {
    super('five-weekly-pay-significant-changes-other-specify')
  }

  setFiveWeeklyPaySignificantChangesOtherSpecifyAnswer(value) {
    browser.setValue('[name="five-weekly-pay-significant-changes-other-specify-answer"]', value)
    return this
  }

  getFiveWeeklyPaySignificantChangesOtherSpecifyAnswer(value) {
    return browser.element('[name="five-weekly-pay-significant-changes-other-specify-answer"]').getValue()
  }

}

export default new FiveWeeklyPaySignificantChangesOtherSpecifyPage()
