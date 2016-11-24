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

  clickEnglishOrWelsh() {
    browser.element('[id="language-welsh-answer-1"]').click()
    return this
  }

  clickOther() {
    browser.element('[id="language-welsh-answer-2"]').click()
    return this
  }

}

export default new LanguagePage()
