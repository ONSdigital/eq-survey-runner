// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FourWeeklyPayGrossPayPage extends QuestionPage {

  constructor() {
    super('four-weekly-pay-gross-pay')
  }

  setFourWeeklyPayGrossPayAnswer(value) {
    browser.setValue('[name="four-weekly-pay-gross-pay-answer"]', value)
    return this
  }

  getFourWeeklyPayGrossPayAnswer(value) {
    return browser.element('[name="four-weekly-pay-gross-pay-answer"]').getValue()
  }

}

export default new FourWeeklyPayGrossPayPage()
