import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class LanguagePage extends MultipleChoiceWithOtherPage {

  clickEnglish() {
    browser.element('[id="language-answer-1"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="language-answer-2"]').click()
    return this
  }

  setLanguageAnswer(value) {
    browser.setValue('[name="language-answer"]', value)
    return this
  }

  getLanguageAnswer(value) {
    return browser.element('[name="language-answer"]').getValue()
  }

  clickEnglishOrWelsh() {
    browser.element('[id="language-welsh-answer-1"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="language-welsh-answer-2"]').click()
    return this
  }

  setLanguageWelshAnswer(value) {
    browser.setValue('[name="language-welsh-answer"]', value)
    return this
  }

  getLanguageWelshAnswer(value) {
    return browser.element('[name="language-welsh-answer"]').getValue()
  }

}

export default new LanguagePage()
