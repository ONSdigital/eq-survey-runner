import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LanguagePage extends MultipleChoiceWithOtherPage {

  clickLanguageAnswerEnglish() {
    browser.element('[id="language-answer-1"]').click()
    return this
  }

  clickLanguageAnswerOther() {
    browser.element('[id="language-answer-2"]').click()
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
