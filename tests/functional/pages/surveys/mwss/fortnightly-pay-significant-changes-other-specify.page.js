// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FortnightlyPaySignificantChangesOtherSpecifyPage extends QuestionPage {

  constructor() {
    super('fortnightly-pay-significant-changes-other-specify')
  }

  setFortnightlyPaySignificantChangesOtherSpecifyAnswer(value) {
    browser.setValue('[name="fortnightly-pay-significant-changes-other-specify-answer"]', value)
    return this
  }

  getFortnightlyPaySignificantChangesOtherSpecifyAnswer(value) {
    return browser.element('[name="fortnightly-pay-significant-changes-other-specify-answer"]').getValue()
  }

}

export default new FortnightlyPaySignificantChangesOtherSpecifyPage()
