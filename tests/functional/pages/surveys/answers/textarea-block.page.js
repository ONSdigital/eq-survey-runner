// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class TextareaBlockPage extends QuestionPage {

  constructor() {
    super('textarea-block')
  }

  setAnswer(value) {
    browser.setValue('[name="answer"]', value)
    return this
  }

  getAnswer(value) {
    return browser.element('[name="answer"]').getValue()
  }

  getAnswerLabel() {
    return browser.element('#label-answer')
  }

  getAnswerElement() {
    return browser.element('[name="answer"]')
  }

}

export default new TextareaBlockPage()
