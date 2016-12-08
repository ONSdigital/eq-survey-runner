// >>> WARNING THIS PAGE WAS AUTO-GENERATED ON 2016-12-13 15:55:57.813972 - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LanguagePage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('language')
  }

  clickLanguageEnglandAnswerEnglish() {
    browser.element('[id="language-england-answer-1"]').click()
    return this
  }

  clickLanguageEnglandAnswerOther() {
    browser.element('[id="language-england-answer-2"]').click()
    return this
  }

  clickLanguageWelshAnswerEnglishOrWelsh() {
    browser.element('[id="language-welsh-answer-1"]').click()
    return this
  }

  clickLanguageWelshAnswerOther() {
    browser.element('[id="language-welsh-answer-2"]').click()
    return this
  }

}

export default new LanguagePage()
