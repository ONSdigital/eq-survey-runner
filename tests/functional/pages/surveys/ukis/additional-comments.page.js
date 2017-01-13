// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class AdditionalCommentsPage extends QuestionPage {

  constructor() {
    super('additional-comments')
  }

  setAdditionalCommentsAnswer(value) {
    browser.setValue('[name="additional-comments-answer"]', value)
    return this
  }

  getAdditionalCommentsAnswer(value) {
    return browser.element('[name="additional-comments-answer"]').getValue()
  }

}

export default new AdditionalCommentsPage()
