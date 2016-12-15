// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.750635 - DO NOT EDIT!!! <<<

import QuestionPage from '../../question.page'

class CorrectNamePage extends QuestionPage {

  constructor() {
    super('correct-name')
  }

  setCorrectFirstName(value) {
    browser.setValue('[name="correct-first-name"]', value)
    return this
  }

  getCorrectFirstName(value) {
    return browser.element('[name="correct-first-name"]').getValue()
  }

  setCorrectMiddleNames(value) {
    browser.setValue('[name="correct-middle-names"]', value)
    return this
  }

  getCorrectMiddleNames(value) {
    return browser.element('[name="correct-middle-names"]').getValue()
  }

  setCorrectLastName(value) {
    browser.setValue('[name="correct-last-name"]', value)
    return this
  }

  getCorrectLastName(value) {
    return browser.element('[name="correct-last-name"]').getValue()
  }

}

export default new CorrectNamePage()
