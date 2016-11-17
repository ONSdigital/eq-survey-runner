import QuestionPage from '../../question.page'

class UnderstandWelshPage extends QuestionPage {

  clickUnderstandSpokenWelsh() {
    browser.element('[id="understand-welsh-answer-1"]').click()
    return this
  }

  clickSpeakWelsh() {
    browser.element('[id="understand-welsh-answer-2"]').click()
    return this
  }

  clickReadWelsh() {
    browser.element('[id="understand-welsh-answer-3"]').click()
    return this
  }

  clickWriteWelsh() {
    browser.element('[id="understand-welsh-answer-4"]').click()
    return this
  }

  clickNoneOfTheAbove() {
    browser.element('[id="understand-welsh-answer-5"]').click()
    return this
  }

  setUnderstandWelshAnswer(value) {
    browser.setValue('[name="understand-welsh-answer"]', value)
    return this
  }

  getUnderstandWelshAnswer(value) {
    return browser.element('[name="understand-welsh-answer"]').getValue()
  }

}

export default new UnderstandWelshPage()
