// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import QuestionPage from '../question.page'

class ChangeCommentBlockPage extends QuestionPage {
  constructor() {
    super('change-comment-block')
  }
  setChangeComment(value) {
    browser.setValue('[name="change-comment"]', value)
    return this
  }
  getChangeComment(value) {
    return browser.element('[name="change-comment"]').getValue()
  }
  getChangeCommentLabel() {
    return browser.element('#label-change-comment')
  }
  getChangeCommentElement() {
    return browser.element('[name="change-comment"]')
  }
}

export default new ChangeCommentBlockPage()
