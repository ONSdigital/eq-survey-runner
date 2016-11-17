import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class PermanentOrFamilyHomePage extends MultipleChoiceWithOtherPage {

  clickYes() {
    browser.element('[id="permanent-or-family-home-answer-1"]').click()
    return this
  }

  clickNo() {
    browser.element('[id="permanent-or-family-home-answer-2"]').click()
    return this
  }

  setPermanentOrFamilyHomeAnswer(value) {
    browser.setValue('[name="permanent-or-family-home-answer"]', value)
    return this
  }

  getPermanentOrFamilyHomeAnswer(value) {
    return browser.element('[name="permanent-or-family-home-answer"]').getValue()
  }

}

export default new PermanentOrFamilyHomePage()
