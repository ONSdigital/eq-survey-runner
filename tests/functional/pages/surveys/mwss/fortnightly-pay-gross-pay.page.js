// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class FortnightlyPayGrossPayPage extends QuestionPage {

  constructor() {
    super('fortnightly-pay-gross-pay')
  }

  setFortnightlyPayGrossPayAnswer(value) {
    browser.setValue('[name="fortnightly-pay-gross-pay-answer"]', value)
    return this
  }

  getFortnightlyPayGrossPayAnswer(value) {
    return browser.element('[name="fortnightly-pay-gross-pay-answer"]').getValue()
  }

}

export default new FortnightlyPayGrossPayPage()
