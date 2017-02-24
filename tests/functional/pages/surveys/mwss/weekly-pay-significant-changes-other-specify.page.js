// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class WeeklyPaySignificantChangesOtherSpecifyPage extends QuestionPage {

  constructor() {
    super('weekly-pay-significant-changes-other-specify')
  }

  setWeeklyPaySignificantChangesOtherSpecifyAnswer(value) {
    browser.setValue('[name="weekly-pay-significant-changes-other-specify-answer"]', value)
    return this
  }

  getWeeklyPaySignificantChangesOtherSpecifyAnswer(value) {
    return browser.element('[name="weekly-pay-significant-changes-other-specify-answer"]').getValue()
  }

}

export default new WeeklyPaySignificantChangesOtherSpecifyPage()
