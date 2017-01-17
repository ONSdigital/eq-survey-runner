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

  clickLanguageWelshAnswerEnglishOrWelsh() {
    browser.element('[id="language-welsh-answer-0"]').click()
    return this
  }

  clickLanguageWelshAnswerOther() {
    browser.element('[id="language-welsh-answer-1"]').click()
    return this
  }

}

export default new LanguagePage()
