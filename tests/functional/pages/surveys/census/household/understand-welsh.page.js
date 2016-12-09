// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-12 22:01:11.895185 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class UnderstandWelshPage extends MultipleChoiceWithOtherPage {

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
