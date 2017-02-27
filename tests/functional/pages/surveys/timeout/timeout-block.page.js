// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class TimeoutBlockPage extends QuestionPage {

  constructor() {
    super('timeout-block')
  }

  setTimeoutAnswer(value) {
    browser.setValue('[name="timeout-answer"]', value)
    return this
  }

  getTimeoutAnswer(value) {
    return browser.element('[name="timeout-answer"]').getValue()
  }

}

export default new TimeoutBlockPage()
