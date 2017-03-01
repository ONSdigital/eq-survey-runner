// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class GeneralCommentsPage extends QuestionPage {

  constructor() {
    super('general-comments')
  }

  setGeneralCommentsAnswer(value) {
    browser.setValue('[name="general-comments-answer"]', value)
    return this
  }

  getGeneralCommentsAnswer(value) {
    return browser.element('[name="general-comments-answer"]').getValue()
  }

}

export default new GeneralCommentsPage()
