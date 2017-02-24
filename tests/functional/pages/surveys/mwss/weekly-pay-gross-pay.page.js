// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class WeeklyPayGrossPayPage extends QuestionPage {

  constructor() {
    super('weekly-pay-gross-pay')
  }

  setWeeklyPayGrossPayAnswer(value) {
    browser.setValue('[name="weekly-pay-gross-pay-answer"]', value)
    return this
  }

  getWeeklyPayGrossPayAnswer(value) {
    return browser.element('[name="weekly-pay-gross-pay-answer"]').getValue()
  }

}

export default new WeeklyPayGrossPayPage()
