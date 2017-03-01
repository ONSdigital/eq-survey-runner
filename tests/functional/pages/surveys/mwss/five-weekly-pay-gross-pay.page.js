// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FiveWeeklyPayGrossPayPage extends QuestionPage {

  constructor() {
    super('five-weekly-pay-gross-pay')
  }

  setFiveWeeklyPayGrossPayAnswer(value) {
    browser.setValue('[name="five-weekly-pay-gross-pay-answer"]', value)
    return this
  }

  getFiveWeeklyPayGrossPayAnswer(value) {
    return browser.element('[name="five-weekly-pay-gross-pay-answer"]').getValue()
  }

}

export default new FiveWeeklyPayGrossPayPage()
