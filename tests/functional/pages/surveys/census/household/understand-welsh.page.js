// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.812491 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class UnderstandWelshPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('understand-welsh')
  }

  clickUnderstandWelshAnswerUnderstandSpokenWelsh() {
    browser.element('[id="understand-welsh-answer-1"]').click()
    return this
  }

  clickUnderstandWelshAnswerSpeakWelsh() {
    browser.element('[id="understand-welsh-answer-2"]').click()
    return this
  }

  clickUnderstandWelshAnswerReadWelsh() {
    browser.element('[id="understand-welsh-answer-3"]').click()
    return this
  }

  clickUnderstandWelshAnswerWriteWelsh() {
    browser.element('[id="understand-welsh-answer-4"]').click()
    return this
  }

  clickUnderstandWelshAnswerNoneOfTheAbove() {
    browser.element('[id="understand-welsh-answer-5"]').click()
    return this
  }

}

export default new UnderstandWelshPage()
