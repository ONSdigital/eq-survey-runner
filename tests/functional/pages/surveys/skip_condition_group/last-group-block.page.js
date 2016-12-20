// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class LastGroupBlockPage extends QuestionPage {

  constructor() {
    super('last-group-block')
  }

  setLastGroupAnswer(value) {
    browser.setValue('[name="last-group-answer"]', value)
    return this
  }

  getLastGroupAnswer(value) {
    return browser.element('[name="last-group-answer"]').getValue()
  }

}

export default new LastGroupBlockPage()
