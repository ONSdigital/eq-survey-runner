// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LanguagePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('language')
  }

  clickLanguageEnglandAnswerEnglish() {
    browser.element('[id="language-england-answer-0"]').click()
    return this
  }

  clickLanguageEnglandAnswerOther() {
    browser.element('[id="language-england-answer-1"]').click()
    return this
  }

  setLanguageEnglandAnswerOther(value) {
    browser.setValue('[name="language-england-answer-other"]', value)
    return this
  }

  getLanguageEnglandAnswerOther(value) {
    return browser.element('[name="language-england-answer-other"]').getValue()
  }

  clickLanguageWelshAnswerEnglishOrWelsh() {
    browser.element('[id="language-welsh-answer-0"]').click()
    return this
  }

  clickLanguageWelshAnswerOther() {
    browser.element('[id="language-welsh-answer-1"]').click()
    return this
  }

  setLanguageWelshAnswerOther(value) {
    browser.setValue('[name="language-welsh-answer-other"]', value)
    return this
  }

  getLanguageWelshAnswerOther(value) {
    return browser.element('[name="language-welsh-answer-other"]').getValue()
  }

}

export default new LanguagePage()
