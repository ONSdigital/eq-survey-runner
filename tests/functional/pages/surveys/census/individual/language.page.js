import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LanguagePage extends MultipleChoiceWithOtherPage {

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
