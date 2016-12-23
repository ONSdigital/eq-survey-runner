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

  setLanguageEnglandAnswerOtherText(value) {
    browser.setValue('[id="language-england-answer-other"]', value)
    return this
  }

  clickLanguageWelshAnswerEnglishOrWelsh() {
    browser.element('[id="language-welsh-answer-0"]').click()
    return this
  }

  clickLanguageWelshAnswerOther() {
    browser.element('[id="language-welsh-answer-1"]').click()
    return this
  }

  setLanguageWelshAnswerOtherText(value) {
    browser.setValue('[id="language-welsh-answer-other"]', value)
    return this
  }

}

export default new LanguagePage()
