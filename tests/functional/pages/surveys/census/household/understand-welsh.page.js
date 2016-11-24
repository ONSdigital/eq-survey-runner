import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class UnderstandWelshPage extends MultipleChoiceWithOtherPage {

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

}

export default new UnderstandWelshPage()
